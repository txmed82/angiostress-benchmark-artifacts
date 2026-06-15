#!/usr/bin/env python3
"""Scaled CathAction human-segmentation subset check for the frozen model panel."""

from __future__ import annotations

import argparse
import gc
import importlib.util
import io
import json
import platform
import sys
import zipfile
from pathlib import Path
from typing import Any

import numpy as np
import torch
from PIL import Image


RUN_ID = "s3f-cathaction-human-segmentation-subset-ranking"
GCP_SOURCE = "gs://seldinger-datasets-raw/angiostress/cathaction/hf/segmentation_human_train.zip"
ZIP_SHA256 = "087c8f971e0455ad67d092a944df75ee7244cbead10e1091c26046ea271e2cf5"
ROUTE_DECISION = "decision-21f6663a"


def load_s2c_module(workspace_root: Path) -> Any:
    script = (
        workspace_root
        / "experiments/main/run-angiostress-s2c-third-frozen-model-panel-extension/run_model_panel_smoke.py"
    )
    spec = importlib.util.spec_from_file_location("s2c_model_panel", script)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import S2c helpers from {script}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def deterministic_indices(total: int, count: int) -> list[int]:
    if count <= 0 or count >= total:
        return list(range(total))
    return sorted({int(x) for x in np.linspace(0, total - 1, count)})


def mask_has_foreground(zf: zipfile.ZipFile, mask_name: str) -> bool:
    mask = Image.open(io.BytesIO(zf.read(mask_name))).convert("L")
    return bool((np.asarray(mask) > 0).any())


def pair_records(zip_path: Path, sample_count: int) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    with zipfile.ZipFile(zip_path) as zf:
        names = set(zf.namelist())
        images = sorted(n for n in names if n.startswith("human_dataset_train/img/") and n.endswith(".jpg"))
        pairs = []
        matched_pair_count = 0
        empty_mask_count = 0
        for image_name in images:
            stem = Path(image_name).stem
            mask_name = f"human_dataset_train/mask/{stem}_mask.png"
            if mask_name in names:
                matched_pair_count += 1
                if mask_has_foreground(zf, mask_name):
                    pairs.append({"pair_id": stem, "image_name": image_name, "mask_name": mask_name})
                else:
                    empty_mask_count += 1
        if not pairs:
            raise RuntimeError(f"no nonempty paired CathAction image/mask records found in {zip_path}")
        metadata = {
            "total_image_mask_pairs": matched_pair_count,
            "nonempty_mask_pairs": len(pairs),
            "empty_mask_pairs_excluded": empty_mask_count,
            "selection_universe": "deterministic_evenly_spaced_over_nonempty_paired_records",
        }
        return [pairs[i] for i in deterministic_indices(len(pairs), sample_count)], metadata


def read_pair(zf: zipfile.ZipFile, record: dict[str, Any]) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    image = Image.open(io.BytesIO(zf.read(record["image_name"]))).convert("RGB")
    mask = Image.open(io.BytesIO(zf.read(record["mask_name"]))).convert("L")
    image_rgb = np.asarray(image, dtype=np.uint8)
    image_gray = np.asarray(image.convert("L"), dtype=np.uint8)
    target = np.asarray(mask) > 0
    if not target.any():
        raise ValueError(f"empty CathAction mask for {record['pair_id']}")
    return image_rgb, image_gray, target


def evaluate_model(
    s2c: Any,
    predictor: Any,
    model: dict[str, Any],
    zip_path: Path,
    pairs: list[dict[str, Any]],
    out_dir: Path,
    bbox_margin: int,
) -> list[dict[str, Any]]:
    pred_dir = out_dir / "cathaction_predictions" / model["model_id"]
    overlay_dir = out_dir / "cathaction_overlays" / model["model_id"]
    pred_dir.mkdir(parents=True, exist_ok=True)
    overlay_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    with zipfile.ZipFile(zip_path) as zf:
        for record in pairs:
            image_rgb, image_gray, target = read_pair(zf, record)
            box = s2c.bbox_from_mask(target, margin=bbox_margin)
            pred, score = s2c.predict_mask(predictor, image_rgb, box)
            pred_path = pred_dir / f"{record['pair_id']}_mask.npy"
            pred_png_path = pred_dir / f"{record['pair_id']}_mask.png"
            overlay_path = overlay_dir / f"{record['pair_id']}_overlay.png"
            np.save(pred_path, pred)
            s2c.save_mask_png(pred_png_path, pred)
            s2c.save_overlay(overlay_path, image_gray, target, pred)
            pred_area = int(pred.sum())
            target_area = int(target.sum())
            rows.append(
                {
                    "model_id": model["model_id"],
                    "surface": "cathaction_human_segmentation_train",
                    "pair_id": record["pair_id"],
                    "image_name": record["image_name"],
                    "mask_name": record["mask_name"],
                    "prediction_path": str(pred_path.relative_to(out_dir)),
                    "prediction_png_path": str(pred_png_path.relative_to(out_dir)),
                    "overlay_path": str(overlay_path.relative_to(out_dir)),
                    "prompt_source": "CathAction mask bbox; subset oracle prompt, not deployable",
                    "prompt_box_xyxy": [float(x) for x in box.tolist()],
                    "sam_score": float(score),
                    "dice": s2c.dice(pred, target),
                    "cldice": s2c.cldice(pred, target),
                    "pred_area_pixels": pred_area,
                    "gt_area_pixels": target_area,
                    "area_ratio": float(pred_area / max(target_area, 1)),
                    "pred_component_count": s2c.component_count(pred),
                    "gt_component_count": s2c.component_count(target),
                }
            )
    return rows


def summarize_models(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    summary = []
    for model_id in sorted({r["model_id"] for r in rows}):
        selected = [r for r in rows if r["model_id"] == model_id]
        summary.append(
            {
                "model_id": model_id,
                "cathaction_sample_mean_dice": float(np.mean([r["dice"] for r in selected])),
                "cathaction_sample_mean_cldice": float(np.mean([r["cldice"] for r in selected])),
                "cathaction_sample_min_dice": float(np.min([r["dice"] for r in selected])),
                "cathaction_sample_min_cldice": float(np.min([r["cldice"] for r in selected])),
                "cathaction_prediction_nonempty_rate": float(np.mean([r["pred_area_pixels"] > 0 for r in selected])),
                "cathaction_sample_mean_area_ratio": float(np.mean([r["area_ratio"] for r in selected])),
            }
        )
    return summary


def ordering_comparison(s2c: Any, workspace_root: Path, summary_rows: list[dict[str, Any]]) -> dict[str, Any]:
    s2c_summary_path = (
        workspace_root
        / "experiments/main/run-angiostress-s2c-third-frozen-model-panel-extension/outputs/model_summary.json"
    )
    s2c_rows = read_json(s2c_summary_path)["rows"]
    synthetic_by_model = {r["model_id"]: float(r["synthetic_mean_stressor_dice"]) for r in s2c_rows}
    shared_models = [r["model_id"] for r in summary_rows if r["model_id"] in synthetic_by_model]
    cathaction_by_model = {r["model_id"]: float(r["cathaction_sample_mean_dice"]) for r in summary_rows}
    synthetic_values = [synthetic_by_model[m] for m in shared_models]
    cathaction_values = [cathaction_by_model[m] for m in shared_models]
    return {
        "ranked_model_count": len(shared_models),
        "synthetic_mean_stressor_dice_order": sorted(shared_models, key=lambda m: synthetic_by_model[m], reverse=True),
        "cathaction_sample_mean_dice_order": sorted(shared_models, key=lambda m: cathaction_by_model[m], reverse=True),
        "spearman_synthetic_mean_stressor_dice_vs_cathaction_mean_dice": s2c.spearman_rank(
            synthetic_values, cathaction_values
        ),
        "rank_correlation_status": "subset_rank_diagnostic_bootstrap_stability_no_final_ci_n3",
        "claim_boundary": (
            "This is a bounded CathAction human-segmentation subset check. It tests whether the frozen-panel "
            "ordering is stable enough to justify paper-outline repair, but it is not the final DIAS + "
            "CathAction construct-validity estimate across all stressors."
        ),
    }


def stability_summary(
    s2c: Any,
    workspace_root: Path,
    rows: list[dict[str, Any]],
    model_summary: list[dict[str, Any]],
    bootstrap_iterations: int,
    bootstrap_seed: int,
) -> dict[str, Any]:
    s2c_summary_path = (
        workspace_root
        / "experiments/main/run-angiostress-s2c-third-frozen-model-panel-extension/outputs/model_summary.json"
    )
    s2c_rows = read_json(s2c_summary_path)["rows"]
    synthetic_by_model = {r["model_id"]: float(r["synthetic_mean_stressor_dice"]) for r in s2c_rows}
    shared_models = [r["model_id"] for r in model_summary if r["model_id"] in synthetic_by_model]
    full_by_model = {r["model_id"]: float(r["cathaction_sample_mean_dice"]) for r in model_summary}
    full_order = sorted(shared_models, key=lambda m: full_by_model[m], reverse=True)
    synthetic_order = sorted(shared_models, key=lambda m: synthetic_by_model[m], reverse=True)
    by_pair_model = {(r["pair_id"], r["model_id"]): float(r["dice"]) for r in rows}
    pair_ids = sorted({r["pair_id"] for r in rows})
    rng = np.random.default_rng(bootstrap_seed)
    spearman_values = []
    full_order_matches = 0
    synthetic_order_matches = 0
    for _ in range(max(bootstrap_iterations, 0)):
        sampled = rng.choice(pair_ids, size=len(pair_ids), replace=True)
        sampled_by_model = {
            model_id: float(np.mean([by_pair_model[(pair_id, model_id)] for pair_id in sampled]))
            for model_id in shared_models
        }
        order = sorted(shared_models, key=lambda m: sampled_by_model[m], reverse=True)
        if order == full_order:
            full_order_matches += 1
        if order == synthetic_order:
            synthetic_order_matches += 1
        spearman = s2c.spearman_rank(
            [synthetic_by_model[m] for m in shared_models],
            [sampled_by_model[m] for m in shared_models],
        )
        if spearman is not None:
            spearman_values.append(float(spearman))
    if spearman_values:
        ci_low, ci_high = np.percentile(spearman_values, [2.5, 97.5])
        spearman_mean = float(np.mean(spearman_values))
    else:
        ci_low = ci_high = spearman_mean = None
    return {
        "bootstrap_iterations": int(bootstrap_iterations),
        "bootstrap_seed": int(bootstrap_seed),
        "sampled_pair_count": len(pair_ids),
        "full_cathaction_order": full_order,
        "synthetic_order": synthetic_order,
        "bootstrap_order_match_full_rate": float(full_order_matches / max(bootstrap_iterations, 1)),
        "bootstrap_order_match_synthetic_rate": float(synthetic_order_matches / max(bootstrap_iterations, 1)),
        "bootstrap_spearman_mean": spearman_mean,
        "bootstrap_spearman_ci95_percentile": [
            None if ci_low is None else float(ci_low),
            None if ci_high is None else float(ci_high),
        ],
        "boundary": (
            "Bootstrap resamples the fixed CathAction subset only; it is a sample-stability diagnostic, "
            "not a population-level final CI."
        ),
    }


def cleanup_zip(zip_path: Path, workspace_root: Path, requested: bool) -> dict[str, Any]:
    status = {
        "delete_requested": requested,
        "zip_path": str(zip_path),
        "exists_before_cleanup": zip_path.exists(),
        "deleted": False,
        "exists_after_cleanup": zip_path.exists(),
    }
    if not requested:
        return status
    resolved = zip_path.resolve()
    tmp_root = (workspace_root / "tmp").resolve()
    if tmp_root not in resolved.parents:
        raise ValueError(f"refusing to delete zip outside workspace tmp/: {resolved}")
    if zip_path.exists():
        zip_path.unlink()
        status["deleted"] = True
    status["exists_after_cleanup"] = zip_path.exists()
    return status


def write_run_notes(
    out_dir: Path,
    args: argparse.Namespace,
    device: str,
    pairs: list[dict[str, Any]],
    pair_metadata: dict[str, Any],
    metrics: dict[str, float],
    model_summary: list[dict[str, Any]],
    order_compare: dict[str, Any],
    stability: dict[str, Any],
    cleanup_status: dict[str, Any],
) -> None:
    command = " ".join(sys.argv)
    run_md = f"""# S3f CathAction Human Segmentation Subset Ranking

## Identity

- run_id: `{RUN_ID}`
- parent_run_id: `run-angiostress-s2c-third-frozen-model-panel-extension`
- route_decision: `{ROUTE_DECISION}`
- storage_decision: `decision-06a3b189`
- command: `{command}`
- device: `{device}`

## Inputs

- CathAction retained zip: `{GCP_SOURCE}`
- Local zip path during run: `{args.zip_path}`
- Local zip source sha256: `{ZIP_SHA256}`
- Sample count per model: `{len(pairs)}`
- Pair selection: deterministic evenly spaced index selection over nonempty human-mask pairs.
- Pair universe: `{pair_metadata["nonempty_mask_pairs"]}` nonempty pairs from `{pair_metadata["total_image_mask_pairs"]}` image-mask pairs; `{pair_metadata["empty_mask_pairs_excluded"]}` empty masks excluded before sampling.
- Model panel: SAM ViT-B, MedSAM ViT-B, and SAM ViT-L, all frozen.
- Bootstrap stability: `{stability["bootstrap_iterations"]}` deterministic resamples over the fixed sampled pair ids.

## Method

The runner imports the S2c frozen-panel helpers for checkpoint verification, SAM predictor construction, bbox prompting, Dice/clDice, and overlay rendering. It reads sampled JPG/PNG pairs directly from the zip into memory without extracting the archive. Prompts are CathAction mask-derived bounding boxes for measurement plumbing only. Stability is estimated by deterministic bootstrap resampling over the fixed sampled pair ids.

## Claim Boundary

This is a scaled CathAction human-segmentation subset check. It tests whether the frozen panel's CathAction ordering is stable enough to justify paper-outline repair and later construct-validity mapping. It does not estimate final DIAS + CathAction construct validity across all stressors or clinical accuracy.
"""
    validation_md = f"""# Validation

## Checks

- outputs_exist: true
- finite_metric_check: `{metrics["s3f_finite_metric_check"]}`
- model_count: `{metrics["s3f_model_count"]}`
- sample_count_per_model: `{metrics["s3f_sample_count_per_model"]}`
- total_prediction_count: `{metrics["s3f_total_prediction_count"]}`
- local_zip_exists_after_cleanup: `{cleanup_status["exists_after_cleanup"]}`

## Model Summary Rows

{json.dumps(model_summary, indent=2)}

## Ordering Boundary

{json.dumps(order_compare, indent=2)}

## Bootstrap Stability

{json.dumps(stability, indent=2)}

## Cleanup

{json.dumps(cleanup_status, indent=2)}

## Caveats

- The sample is deterministic and still limited to the human-segmentation training archive; it is a subset stability diagnostic, not a final powered construct-validity estimate.
- Prompts are label-derived oracle boxes, not deployable prompts.
- Larger CathAction payloads were not downloaded.
"""
    (out_dir.parent / "RUN.md").write_text(run_md)
    (out_dir.parent / "VALIDATION.md").write_text(validation_md)


def evaluate_all(args: argparse.Namespace, device: str) -> dict[str, Any]:
    workspace_root = args.workspace_root.resolve()
    out_dir = args.out.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    s2c = load_s2c_module(workspace_root)
    pairs, pair_metadata = pair_records(args.zip_path, args.sample_count)
    print(f"s3f_sampled_pair_count={len(pairs)}", flush=True)
    print(f"s3f_empty_mask_pairs_excluded={pair_metadata['empty_mask_pairs_excluded']}", flush=True)
    model_records = []
    rows: list[dict[str, Any]] = []
    for model in s2c.MODEL_PANEL:
        print(f"s3f_evaluating_model={model['model_id']}", flush=True)
        predictor, checkpoint_sha = s2c.build_predictor(model, device)
        model_records.append(
            {
                **{k: v for k, v in model.items() if k != "checkpoint"},
                "checkpoint_path": model["checkpoint"],
                "verified_checkpoint_sha256": checkpoint_sha,
            }
        )
        rows.extend(evaluate_model(s2c, predictor, model, args.zip_path, pairs, out_dir, args.bbox_margin))
        del predictor
        gc.collect()
        if device == "mps":
            torch.mps.empty_cache()

    model_summary = summarize_models(rows)
    order_compare = ordering_comparison(s2c, workspace_root, model_summary)
    stability = stability_summary(
        s2c,
        workspace_root,
        rows,
        model_summary,
        args.bootstrap_iterations,
        args.bootstrap_seed,
    )
    metrics: dict[str, float] = {
        **s2c.BASELINE_METRICS,
        "s3f_model_count": float(len(s2c.MODEL_PANEL)),
        "s3f_sample_count_per_model": float(len(pairs)),
        "s3f_total_prediction_count": float(len(rows)),
        "s3f_ranked_model_count": float(len(model_summary)),
        "s3f_nonempty_pair_universe_count": float(pair_metadata["nonempty_mask_pairs"]),
        "s3f_empty_mask_pairs_excluded_count": float(pair_metadata["empty_mask_pairs_excluded"]),
        "s3f_bootstrap_order_match_full_rate": float(stability["bootstrap_order_match_full_rate"]),
        "s3f_bootstrap_order_match_synthetic_rate": float(stability["bootstrap_order_match_synthetic_rate"]),
        "s3f_bootstrap_spearman_mean": float(stability["bootstrap_spearman_mean"]),
        "s3f_bootstrap_spearman_ci95_low": float(stability["bootstrap_spearman_ci95_percentile"][0]),
        "s3f_bootstrap_spearman_ci95_high": float(stability["bootstrap_spearman_ci95_percentile"][1]),
        "s3f_finite_metric_check": 1.0,
    }
    for row in model_summary:
        prefix = f"s3f_{row['model_id']}"
        for key, value in row.items():
            if key == "model_id":
                continue
            metrics[f"{prefix}_{key}"] = float(value)
    spearman = order_compare["spearman_synthetic_mean_stressor_dice_vs_cathaction_mean_dice"]
    if spearman is not None:
        metrics["s3f_spearman_synthetic_mean_vs_cathaction_mean_dice"] = float(spearman)
    if not all(np.isfinite(v) for v in metrics.values() if isinstance(v, (float, int))):
        metrics["s3f_finite_metric_check"] = 0.0
        raise ValueError("nonfinite metric detected")

    s2c.write_csv(out_dir / "per_pair_metrics.csv", rows)
    write_json(out_dir / "per_pair_metrics.json", {"rows": rows})
    s2c.write_csv(out_dir / "model_summary.csv", model_summary)
    write_json(out_dir / "model_summary.json", {"rows": model_summary})
    write_json(out_dir / "model_ranking_rows.json", {"comparison": order_compare})
    write_json(out_dir / "stability_summary.json", stability)
    write_json(out_dir / "metrics_summary.json", metrics)
    write_json(
        out_dir / "manifest.json",
        {
            "run_id": RUN_ID,
            "parent_run_id": "run-angiostress-s2c-third-frozen-model-panel-extension",
            "route_decision": ROUTE_DECISION,
            "storage_decision": "decision-06a3b189",
            "device": device,
            "gcp_source": GCP_SOURCE,
            "zip_sha256": ZIP_SHA256,
            "sample_count": len(pairs),
            "pair_selection": pair_metadata["selection_universe"],
            "pair_universe": pair_metadata,
            "sampled_pairs": pairs,
            "models": model_records,
            "outputs": {
                "per_pair_metrics": "per_pair_metrics.json",
                "model_summary": "model_summary.json",
                "model_ranking_rows": "model_ranking_rows.json",
                "stability_summary": "stability_summary.json",
                "metrics_summary": "metrics_summary.json",
            },
            "claim_boundary": order_compare["claim_boundary"],
        },
    )
    write_json(
        out_dir / "environment.json",
        {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
            "torch": torch.__version__,
            "device": device,
        },
    )
    cleanup_status = cleanup_zip(args.zip_path, workspace_root, args.delete_zip_after_run)
    write_json(out_dir / "cleanup_status.json", cleanup_status)
    write_run_notes(
        out_dir,
        args,
        device,
        pairs,
        pair_metadata,
        metrics,
        model_summary,
        order_compare,
        stability,
        cleanup_status,
    )
    return {
        "metrics": metrics,
        "model_summary_rows": model_summary,
        "ordering_comparison": order_compare,
        "stability_summary": stability,
        "cleanup_status": cleanup_status,
    }


def choose_devices(s2c: Any, requested: str) -> list[str]:
    return s2c.choose_devices(requested)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--zip-path", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--workspace-root", type=Path, default=Path.cwd())
    parser.add_argument("--device", default="auto", choices=["auto", "cpu", "mps", "cuda"])
    parser.add_argument("--sample-count", type=int, default=128)
    parser.add_argument("--bbox-margin", type=int, default=5)
    parser.add_argument("--bootstrap-iterations", type=int, default=1000)
    parser.add_argument("--bootstrap-seed", type=int, default=20260615)
    parser.add_argument("--delete-zip-after-run", action="store_true")
    args = parser.parse_args()

    s2c = load_s2c_module(args.workspace_root.resolve())
    errors = []
    for device in choose_devices(s2c, args.device):
        try:
            result = evaluate_all(args, device)
            print(
                json.dumps(
                    {
                        "run_id": RUN_ID,
                        "device": device,
                        "model_summary_rows": result["model_summary_rows"],
                        "ordering_comparison": result["ordering_comparison"],
                        "stability_summary": result["stability_summary"],
                        "cleanup_status": result["cleanup_status"],
                        "metrics": str((args.out / "metrics_summary.json").resolve()),
                    },
                    indent=2,
                    sort_keys=True,
                )
            )
            return 0
        except Exception as exc:
            errors.append({"device": device, "error": type(exc).__name__, "message": str(exc)})
            if device == choose_devices(s2c, args.device)[-1]:
                args.out.mkdir(parents=True, exist_ok=True)
                write_json(args.out / "BLOCKER.json", {"run_id": RUN_ID, "errors": errors})
                raise
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
