#!/usr/bin/env python3
"""DIAS multi-sequence ranking slice for the AngioStress frozen panel."""

from __future__ import annotations

import argparse
import gc
import importlib.util
import json
import math
import platform
import re
import sys
import zipfile
from collections import defaultdict
from io import BytesIO
from pathlib import Path
from typing import Any

import numpy as np
import torch
from PIL import Image


DEFAULT_SLICE_ID = "s3b-dias-full-test-split-ranking"
DEFAULT_PARENT_RUN_ID = "run-angiostress-s2c-third-frozen-model-panel-extension"
SYNTHETIC_ORDER_SOURCE = (
    "experiments/main/run-angiostress-s2c-third-frozen-model-panel-extension/outputs/model_summary.json"
)
S2C_SCRIPT = (
    "experiments/main/run-angiostress-s2c-third-frozen-model-panel-extension/run_model_panel_smoke.py"
)
DEFAULT_DIAS_ZIP = "tmp/datasets/DIAS/DIAS.zip"


def load_s2c(workspace_root: Path) -> Any:
    script = workspace_root / S2C_SCRIPT
    spec = importlib.util.spec_from_file_location("angiostress_s2c_panel", script)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not import S2c evaluator from {script}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty CSV: {path}")
    import csv

    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_image_member(zf: zipfile.ZipFile, member: str) -> np.ndarray:
    with zf.open(member) as f:
        data = f.read()
    return np.asarray(Image.open(BytesIO(data)).convert("L"))


def discover_test_sequences(zf: zipfile.ZipFile) -> list[dict[str, Any]]:
    frame_re = re.compile(r"^DIAS/test/images/image_(s\d+)_i(\d+)\.png$")
    labels = set(zf.namelist())
    by_sequence: dict[str, list[tuple[int, str]]] = defaultdict(list)
    for name in zf.namelist():
        match = frame_re.match(name)
        if not match:
            continue
        by_sequence[match.group(1)].append((int(match.group(2)), name))

    records = []
    for sequence_id in sorted(by_sequence, key=lambda x: int(x[1:])):
        label_member = f"DIAS/test/labels/label_{sequence_id}.png"
        if label_member not in labels:
            continue
        frame_records = [
            {"frame_index": idx, "frame_member": member}
            for idx, member in sorted(by_sequence[sequence_id], key=lambda x: x[0])
        ]
        records.append(
            {
                "sequence_id": sequence_id,
                "split": "test",
                "label_member": label_member,
                "frame_count": len(frame_records),
                "frame_records": frame_records,
            }
        )
    return records


def select_sequences(
    records: list[dict[str, Any]],
    requested: list[str],
    sequence_count: int,
) -> list[dict[str, Any]]:
    if requested:
        by_id = {r["sequence_id"]: r for r in records}
        missing = [sid for sid in requested if sid not in by_id]
        if missing:
            raise ValueError(f"requested DIAS test sequences not found or unlabeled: {missing}")
        return [by_id[sid] for sid in requested]
    return records[:sequence_count]


def finite_mean(values: list[float]) -> float:
    if not values:
        return float("nan")
    return float(np.mean(np.asarray(values, dtype=np.float64)))


def finite_median(values: list[float]) -> float:
    if not values:
        return float("nan")
    return float(np.median(np.asarray(values, dtype=np.float64)))


def kendall_tau(xs: list[float], ys: list[float]) -> float | None:
    if len(xs) < 3 or len(xs) != len(ys):
        return None
    concordant = discordant = ties = 0
    for i in range(len(xs)):
        for j in range(i + 1, len(xs)):
            dx = xs[i] - xs[j]
            dy = ys[i] - ys[j]
            prod = dx * dy
            if prod > 0:
                concordant += 1
            elif prod < 0:
                discordant += 1
            else:
                ties += 1
    denom = concordant + discordant + ties
    if denom == 0:
        return None
    return float((concordant - discordant) / denom)


def bootstrap_mean_ci(values: list[float], seed: int, draws: int = 2000) -> dict[str, float | None]:
    clean = [float(v) for v in values if math.isfinite(float(v))]
    if not clean:
        return {"mean": None, "ci95_low": None, "ci95_high": None, "draws": 0}
    rng = np.random.default_rng(seed)
    arr = np.asarray(clean, dtype=np.float64)
    sample_means = np.asarray([rng.choice(arr, size=arr.size, replace=True).mean() for _ in range(draws)])
    return {
        "mean": float(arr.mean()),
        "ci95_low": float(np.percentile(sample_means, 2.5)),
        "ci95_high": float(np.percentile(sample_means, 97.5)),
        "draws": draws,
    }


def load_s2c_synthetic_summary(workspace_root: Path) -> tuple[list[dict[str, Any]], dict[str, float]]:
    summary_path = workspace_root / SYNTHETIC_ORDER_SOURCE
    rows = json.loads(summary_path.read_text())["rows"]
    values = {row["model_id"]: float(row["synthetic_mean_stressor_dice"]) for row in rows}
    return rows, values


def evaluate_model(
    s2c: Any,
    zf: zipfile.ZipFile,
    model: dict[str, Any],
    predictor: Any,
    selected_sequences: list[dict[str, Any]],
    out_dir: Path,
    bbox_margin: int,
    max_frames_per_sequence: int,
    save_visuals: bool,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    sequence_rows: list[dict[str, Any]] = []
    pred_dir = out_dir / "predictions" / model["model_id"]
    overlay_dir = out_dir / "overlays" / model["model_id"]
    pred_dir.mkdir(parents=True, exist_ok=True)
    overlay_dir.mkdir(parents=True, exist_ok=True)

    for sequence in selected_sequences:
        target = read_image_member(zf, sequence["label_member"]) > 0
        box = s2c.bbox_from_mask(target, margin=bbox_margin)
        target_area = int(target.sum())
        target_components = s2c.component_count(target)
        frame_records = sequence["frame_records"]
        if max_frames_per_sequence > 0:
            frame_records = frame_records[:max_frames_per_sequence]

        sequence_frame_rows: list[dict[str, Any]] = []
        for frame in frame_records:
            gray = read_image_member(zf, frame["frame_member"])
            pred, score = s2c.predict_mask(predictor, s2c.gray_to_rgb(gray), box)
            frame_index = int(frame["frame_index"])
            stem = f"{sequence['sequence_id']}_frame_{frame_index:02d}"
            pred_path = pred_dir / f"{stem}_mask.npy"
            pred_png_path = pred_dir / f"{stem}_mask.png"
            overlay_path = overlay_dir / f"{stem}_overlay.png"
            np.save(pred_path, pred)
            if save_visuals:
                s2c.save_mask_png(pred_png_path, pred)
                s2c.save_overlay(overlay_path, gray, target, pred)

            pred_area = int(pred.sum())
            pred_components = s2c.component_count(pred)
            row = {
                "model_id": model["model_id"],
                "display_name": model["display_name"],
                "surface": "dias_test_multisequence",
                "sequence_id": sequence["sequence_id"],
                "split": sequence["split"],
                "frame_index": frame_index,
                "frame_count_in_sequence": int(sequence["frame_count"]),
                "frame_member": frame["frame_member"],
                "label_member": sequence["label_member"],
                "prompt_protocol": f"label_bbox_margin_{bbox_margin}",
                "prediction_path": str(pred_path.relative_to(out_dir)),
                "prediction_png_path": str(pred_png_path.relative_to(out_dir)) if save_visuals else None,
                "overlay_path": str(overlay_path.relative_to(out_dir)) if save_visuals else None,
                "intensity_mean": float(np.mean(gray)),
                "intensity_std": float(np.std(gray)),
                "sam_score": float(score),
                "dice": s2c.dice(pred, target),
                "cldice": s2c.cldice(pred, target),
                "pred_area_pixels": pred_area,
                "gt_area_pixels": target_area,
                "area_ratio": float(pred_area / max(target_area, 1)),
                "pred_component_count": pred_components,
                "gt_component_count": target_components,
                "component_count_ratio": float(pred_components / max(target_components, 1)),
            }
            rows.append(row)
            sequence_frame_rows.append(row)

        sequence_rows.append(
            {
                "model_id": model["model_id"],
                "display_name": model["display_name"],
                "surface": "dias_test_multisequence",
                "sequence_id": sequence["sequence_id"],
                "split": sequence["split"],
                "evaluated_frame_count": len(sequence_frame_rows),
                "available_frame_count": int(sequence["frame_count"]),
                "mean_dice": finite_mean([float(r["dice"]) for r in sequence_frame_rows]),
                "median_dice": finite_median([float(r["dice"]) for r in sequence_frame_rows]),
                "mean_cldice": finite_mean([float(r["cldice"]) for r in sequence_frame_rows]),
                "mean_sam_score": finite_mean([float(r["sam_score"]) for r in sequence_frame_rows]),
                "mean_area_ratio": finite_mean([float(r["area_ratio"]) for r in sequence_frame_rows]),
                "gt_area_pixels": target_area,
                "gt_component_count": target_components,
            }
        )
    return rows, sequence_rows


def summarize_models(
    model_rows: list[dict[str, Any]],
    sequence_rows: list[dict[str, Any]],
    s2c_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    by_model = defaultdict(list)
    seq_by_model = defaultdict(list)
    s2c_by_model = {row["model_id"]: row for row in s2c_rows}
    for row in model_rows:
        by_model[row["model_id"]].append(row)
    for row in sequence_rows:
        seq_by_model[row["model_id"]].append(row)

    rows = []
    for model_id in sorted(by_model):
        records = by_model[model_id]
        seq_records = seq_by_model[model_id]
        first = records[0]
        s2c_row = s2c_by_model[model_id]
        rows.append(
            {
                "model_id": model_id,
                "display_name": first["display_name"],
                "evaluated_sequence_count": len(seq_records),
                "evaluated_frame_count": len(records),
                "dias_multisequence_mean_dice": finite_mean([float(r["dice"]) for r in records]),
                "dias_multisequence_median_dice": finite_median([float(r["dice"]) for r in records]),
                "dias_multisequence_mean_cldice": finite_mean([float(r["cldice"]) for r in records]),
                "dias_multisequence_mean_sam_score": finite_mean([float(r["sam_score"]) for r in records]),
                "sequence_mean_dice_mean": finite_mean([float(r["mean_dice"]) for r in seq_records]),
                "sequence_mean_dice_min": float(min(float(r["mean_dice"]) for r in seq_records)),
                "sequence_mean_dice_max": float(max(float(r["mean_dice"]) for r in seq_records)),
                "s2c_synthetic_clean_dice": float(s2c_row["synthetic_clean_dice"]),
                "s2c_synthetic_mean_stressor_dice": float(s2c_row["synthetic_mean_stressor_dice"]),
                "s2c_dias_s40_all_frame_mean_dice": float(s2c_row["dias_all_frame_mean_dice"]),
            }
        )
    return rows


def ranking_diagnostics(
    model_summary: list[dict[str, Any]],
    sequence_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    model_ids = [r["model_id"] for r in model_summary]
    synth_values = [float(r["s2c_synthetic_mean_stressor_dice"]) for r in model_summary]
    dias_values = [float(r["dias_multisequence_mean_dice"]) for r in model_summary]
    synthetic_order = [
        r["model_id"] for r in sorted(model_summary, key=lambda x: float(x["s2c_synthetic_mean_stressor_dice"]), reverse=True)
    ]
    dias_order = [
        r["model_id"] for r in sorted(model_summary, key=lambda x: float(x["dias_multisequence_mean_dice"]), reverse=True)
    ]
    aggregate_spearman = s2c_spearman(synth_values, dias_values)
    aggregate_kendall = kendall_tau(synth_values, dias_values)

    seq_by_id: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
    for row in sequence_rows:
        seq_by_id[row["sequence_id"]][row["model_id"]] = row

    sequence_diagnostics = []
    for sequence_id in sorted(seq_by_id, key=lambda x: int(x[1:])):
        if any(model_id not in seq_by_id[sequence_id] for model_id in model_ids):
            continue
        seq_values = [float(seq_by_id[sequence_id][model_id]["mean_dice"]) for model_id in model_ids]
        seq_order = [
            model_id
            for model_id, _ in sorted(
                zip(model_ids, seq_values),
                key=lambda x: x[1],
                reverse=True,
            )
        ]
        sequence_diagnostics.append(
            {
                "sequence_id": sequence_id,
                "model_order_by_mean_dice": seq_order,
                "spearman_s2c_synthetic_vs_sequence_mean_dice": s2c_spearman(synth_values, seq_values),
                "kendall_s2c_synthetic_vs_sequence_mean_dice": kendall_tau(synth_values, seq_values),
                "per_model_mean_dice": {model_id: seq_by_id[sequence_id][model_id]["mean_dice"] for model_id in model_ids},
            }
        )

    sequence_spearman_values = [
        float(r["spearman_s2c_synthetic_vs_sequence_mean_dice"])
        for r in sequence_diagnostics
        if r["spearman_s2c_synthetic_vs_sequence_mean_dice"] is not None
    ]
    sequence_kendall_values = [
        float(r["kendall_s2c_synthetic_vs_sequence_mean_dice"])
        for r in sequence_diagnostics
        if r["kendall_s2c_synthetic_vs_sequence_mean_dice"] is not None
    ]
    return {
        "ranked_model_count": len(model_summary),
        "model_ids": model_ids,
        "synthetic_order_source": SYNTHETIC_ORDER_SOURCE,
        "s2c_synthetic_mean_stressor_dice_order": synthetic_order,
        "dias_multisequence_mean_dice_order": dias_order,
        "aggregate_spearman_s2c_synthetic_vs_dias_multisequence_mean_dice": aggregate_spearman,
        "aggregate_kendall_s2c_synthetic_vs_dias_multisequence_mean_dice": aggregate_kendall,
        "sequence_rank_diagnostics": sequence_diagnostics,
        "sequence_spearman_bootstrap": bootstrap_mean_ci(sequence_spearman_values, seed=3103),
        "sequence_kendall_bootstrap": bootstrap_mean_ci(sequence_kendall_values, seed=3104),
        "rank_correlation_status": (
            "diagnostic_only_n3_models_sequence_bootstrap_one_synthetic_case_no_cathaction"
        ),
        "claim_boundary": (
            "S3B evaluates the full labeled DIAS test split but remains a construct-validity diagnostic: "
            "one synthetic TopCoW case, oracle label-box prompting, sequence-level DIAS masks, "
            "three frozen promptable models, and no CathAction/device-action analog."
        ),
    }


def s2c_spearman(xs: list[float], ys: list[float]) -> float | None:
    if len(xs) < 3 or len(xs) != len(ys):
        return None
    order_x = np.asarray(descending_ranks(xs), dtype=np.float64)
    order_y = np.asarray(descending_ranks(ys), dtype=np.float64)
    if float(np.std(order_x)) == 0.0 or float(np.std(order_y)) == 0.0:
        return None
    return float(np.corrcoef(order_x, order_y)[0, 1])


def descending_ranks(values: list[float]) -> list[float]:
    order = sorted(range(len(values)), key=lambda i: values[i], reverse=True)
    ranks = [0.0] * len(values)
    start = 0
    while start < len(order):
        end = start + 1
        while end < len(order) and values[order[end]] == values[order[start]]:
            end += 1
        avg_rank = (start + 1 + end) / 2.0
        for idx in order[start:end]:
            ranks[idx] = avg_rank
        start = end
    return ranks


def metrics_summary(model_summary: list[dict[str, Any]], ranking: dict[str, Any], metric_prefix: str) -> dict[str, float]:
    metrics: dict[str, float] = {
        f"{metric_prefix}_model_count": float(len(model_summary)),
        f"{metric_prefix}_sequence_count": float(max(r["evaluated_sequence_count"] for r in model_summary)),
        f"{metric_prefix}_frame_count_per_model": float(max(r["evaluated_frame_count"] for r in model_summary)),
        f"{metric_prefix}_total_prediction_count": float(sum(r["evaluated_frame_count"] for r in model_summary)),
        f"{metric_prefix}_aggregate_spearman_s2c_synthetic_vs_dias_multisequence_mean_dice": float(
            ranking["aggregate_spearman_s2c_synthetic_vs_dias_multisequence_mean_dice"]
        ),
        f"{metric_prefix}_aggregate_kendall_s2c_synthetic_vs_dias_multisequence_mean_dice": float(
            ranking["aggregate_kendall_s2c_synthetic_vs_dias_multisequence_mean_dice"]
        ),
        f"{metric_prefix}_sequence_spearman_mean": float(ranking["sequence_spearman_bootstrap"]["mean"]),
        f"{metric_prefix}_sequence_spearman_ci95_low": float(ranking["sequence_spearman_bootstrap"]["ci95_low"]),
        f"{metric_prefix}_sequence_spearman_ci95_high": float(ranking["sequence_spearman_bootstrap"]["ci95_high"]),
        f"{metric_prefix}_sequence_kendall_mean": float(ranking["sequence_kendall_bootstrap"]["mean"]),
        f"{metric_prefix}_sequence_kendall_ci95_low": float(ranking["sequence_kendall_bootstrap"]["ci95_low"]),
        f"{metric_prefix}_sequence_kendall_ci95_high": float(ranking["sequence_kendall_bootstrap"]["ci95_high"]),
        f"{metric_prefix}_finite_metric_check": 1.0,
    }
    for row in model_summary:
        prefix = f"{metric_prefix}_{row['model_id']}"
        for key in [
            "dias_multisequence_mean_dice",
            "dias_multisequence_median_dice",
            "dias_multisequence_mean_cldice",
            "sequence_mean_dice_mean",
            "s2c_synthetic_mean_stressor_dice",
            "s2c_dias_s40_all_frame_mean_dice",
        ]:
            metrics[f"{prefix}_{key}"] = float(row[key])
    if not all(math.isfinite(v) for v in metrics.values()):
        metrics[f"{metric_prefix}_finite_metric_check"] = 0.0
    return metrics


def write_notes(
    run_dir: Path,
    out_dir: Path,
    slice_id: str,
    parent_run_id: str,
    selected_sequences: list[dict[str, Any]],
    model_summary: list[dict[str, Any]],
    ranking: dict[str, Any],
    metrics: dict[str, float],
    metric_prefix: str,
) -> None:
    sequence_ids = ", ".join(r["sequence_id"] for r in selected_sequences)
    model_lines = "\n".join(
        (
            f"- {r['model_id']}: DIAS multi-sequence Dice {r['dias_multisequence_mean_dice']:.4f}, "
            f"clDice {r['dias_multisequence_mean_cldice']:.4f}, "
            f"S2c synthetic stress Dice {r['s2c_synthetic_mean_stressor_dice']:.4f}"
        )
        for r in model_summary
    )
    run_dir.joinpath("RUN.md").write_text(
        f"""# {slice_id}

## Objective

Expand the real-DIAS side of the S2c three-model frozen panel from one sequence to a deterministic labeled test-sequence subset, while preserving the frozen checkpoints, label-derived box prompt, and Dice/clDice metrics.

## Parent Evidence

- Parent run: `{parent_run_id}`
- Synthetic ordering source: `{SYNTHETIC_ORDER_SOURCE}`
- Selected DIAS test sequences: {sequence_ids}
- Claim boundary: diagnostic precursor only; no full construct-validity claim.

## Result

Synthetic stressor order: `{ranking['s2c_synthetic_mean_stressor_dice_order']}`
DIAS multi-sequence order: `{ranking['dias_multisequence_mean_dice_order']}`

- Aggregate Spearman: `{ranking['aggregate_spearman_s2c_synthetic_vs_dias_multisequence_mean_dice']}`
- Sequence-bootstrap Spearman mean: `{metrics[f'{metric_prefix}_sequence_spearman_mean']:.4f}` with 95% CI `[{metrics[f'{metric_prefix}_sequence_spearman_ci95_low']:.4f}, {metrics[f'{metric_prefix}_sequence_spearman_ci95_high']:.4f}]`

## Model Summary

{model_lines}

## Limitations

- DIAS provides sequence-level vessel labels, reused for each frame.
- The prompt remains an oracle label-derived bounding box, matching S2c and avoiding model tuning.
- The synthetic side is still one TopCoW case.
- CathAction/device-action analog coverage is still blocked by dataset access.
- The bootstrap interval resamples this small sequence subset and is not a final paper-level construct-validity interval.
""",
        encoding="utf-8",
    )
    run_dir.joinpath("VALIDATION.md").write_text(
        f"""# Validation

- Output directory: `{out_dir}`
- Model count: `{int(metrics[f'{metric_prefix}_model_count'])}`
- Sequence count: `{int(metrics[f'{metric_prefix}_sequence_count'])}`
- Frame count per model: `{int(metrics[f'{metric_prefix}_frame_count_per_model'])}`
- Total predictions: `{int(metrics[f'{metric_prefix}_total_prediction_count'])}`
- Finite metric check: `{metrics[f'{metric_prefix}_finite_metric_check']}`
- Required files present: `metrics_summary.json`, `model_summary.json`, `per_frame_metrics.json`, `per_sequence_summary.json`, `ranking_diagnostics.json`, `manifest.json`, `environment.json`
""",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dias-zip", default=DEFAULT_DIAS_ZIP)
    parser.add_argument("--slice-id", default=DEFAULT_SLICE_ID)
    parser.add_argument("--parent-run-id", default=DEFAULT_PARENT_RUN_ID)
    parser.add_argument("--out", default=None)
    parser.add_argument("--sequence-count", type=int, default=20)
    parser.add_argument("--sequences", nargs="*", default=[])
    parser.add_argument("--max-frames-per-sequence", type=int, default=0)
    parser.add_argument("--bbox-margin", type=int, default=5)
    parser.add_argument("--device", choices=["auto", "mps", "cpu"], default="auto")
    parser.add_argument("--no-visuals", action="store_true")
    args = parser.parse_args()

    workspace_root = Path.cwd()
    run_dir = workspace_root / f"experiments/analysis/{args.slice_id}"
    out_rel = args.out or f"experiments/analysis/{args.slice_id}/outputs"
    out_dir = workspace_root / out_rel
    out_dir.mkdir(parents=True, exist_ok=True)
    s2c = load_s2c(workspace_root)
    devices = s2c.choose_devices(args.device)
    device = devices[0]
    dias_zip = Path(args.dias_zip)
    if not dias_zip.exists():
        raise FileNotFoundError(dias_zip)

    s2c_rows, _ = load_s2c_synthetic_summary(workspace_root)
    with zipfile.ZipFile(dias_zip) as zf:
        all_records = discover_test_sequences(zf)
        selected_sequences = select_sequences(all_records, args.sequences, args.sequence_count)
        if len(selected_sequences) < 5 and not args.sequences and args.sequence_count >= 5:
            raise RuntimeError(f"expected at least 5 labeled DIAS test sequences, found {len(selected_sequences)}")
        per_frame_rows: list[dict[str, Any]] = []
        per_sequence_rows: list[dict[str, Any]] = []
        checkpoint_rows = []
        for model in s2c.MODEL_PANEL:
            predictor, actual_sha = s2c.build_predictor(model, device=device)
            checkpoint_rows.append(
                {
                    "model_id": model["model_id"],
                    "model_type": model.get("model_type", "vit_b"),
                    "checkpoint": model["checkpoint"],
                    "checkpoint_sha256": actual_sha,
                    "expected_checkpoint_sha256": model.get("checkpoint_sha256"),
                    "source": model.get("source"),
                }
            )
            rows, seq_rows = evaluate_model(
                s2c=s2c,
                zf=zf,
                model=model,
                predictor=predictor,
                selected_sequences=selected_sequences,
                out_dir=out_dir,
                bbox_margin=args.bbox_margin,
                max_frames_per_sequence=args.max_frames_per_sequence,
                save_visuals=not args.no_visuals,
            )
            per_frame_rows.extend(rows)
            per_sequence_rows.extend(seq_rows)
            del predictor
            gc.collect()
            if torch.backends.mps.is_available():
                torch.mps.empty_cache()

    model_summary = summarize_models(per_frame_rows, per_sequence_rows, s2c_rows)
    ranking = ranking_diagnostics(model_summary, per_sequence_rows)
    metric_prefix = args.slice_id.split("-", 1)[0]
    metrics = metrics_summary(model_summary, ranking, metric_prefix)
    sequence_ids = [r["sequence_id"] for r in selected_sequences]
    manifest = {
        "slice_id": args.slice_id,
        "parent_run_id": args.parent_run_id,
        "dias_zip": str(dias_zip),
        "dias_zip_size_bytes": dias_zip.stat().st_size,
        "dias_zip_sha256": s2c.sha256_file(dias_zip),
        "selected_sequence_ids": sequence_ids,
        "selected_sequences": selected_sequences,
        "available_labeled_test_sequence_count": len(all_records),
        "model_checkpoints": checkpoint_rows,
        "prompt_protocol": f"label_bbox_margin_{args.bbox_margin}",
        "metric_protocol": "Dice and clDice against DIAS sequence-level binary vessel mask per frame.",
        "device": device,
        "max_frames_per_sequence": args.max_frames_per_sequence,
        "claim_boundary": ranking["claim_boundary"],
    }
    environment = {
        "python": sys.version,
        "platform": platform.platform(),
        "torch": torch.__version__,
        "mps_available": bool(torch.backends.mps.is_available()),
        "device": device,
    }

    write_json(out_dir / "metrics_summary.json", metrics)
    write_json(out_dir / "model_summary.json", {"rows": model_summary})
    write_json(out_dir / "per_frame_metrics.json", {"rows": per_frame_rows})
    write_json(out_dir / "per_sequence_summary.json", {"rows": per_sequence_rows})
    write_json(out_dir / "ranking_diagnostics.json", ranking)
    write_json(out_dir / "manifest.json", manifest)
    write_json(out_dir / "environment.json", environment)
    write_csv(out_dir / "per_frame_metrics.csv", per_frame_rows)
    write_csv(out_dir / "per_sequence_summary.csv", per_sequence_rows)
    write_csv(out_dir / "model_summary.csv", model_summary)
    write_notes(run_dir, out_dir, args.slice_id, args.parent_run_id, selected_sequences, model_summary, ranking, metrics, metric_prefix)
    print(json.dumps({"metrics_summary": metrics, "ranking": ranking}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
