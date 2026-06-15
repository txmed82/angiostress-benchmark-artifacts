#!/usr/bin/env python3
"""Frozen SAM smoke on one verified DIAS sequence."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
import sys
from pathlib import Path
from typing import Any

import numpy as np
import torch
from PIL import Image
from segment_anything import SamPredictor, sam_model_registry
from skimage import measure, morphology


RUN_ID = "run-angiostress-s3-dias-frozen-model-analog-smoke"
BASELINE_METRICS = {
    "topcow_resencm_one_case_mean_dice": 0.6984658547796687,
    "topcow_resencm_one_case_mean_cldice": 0.6285484218960072,
    "topcow_resencm_one_case_graph_ready_rate": 1.0,
    "topcow_gt_sanity_mean_dice": 1.0,
    "topcow_gt_sanity_mean_cldice": 1.0,
    "topcow_gt_sanity_graph_ready_rate": 1.0,
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def resolve_path(workspace_root: Path, value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    return (workspace_root / path).resolve()


def load_gray(path: Path) -> np.ndarray:
    return np.asarray(Image.open(path).convert("L"))


def to_rgb(gray: np.ndarray) -> np.ndarray:
    if gray.dtype != np.uint8:
        gray = np.clip(gray, 0, 255).astype(np.uint8)
    return np.stack([gray, gray, gray], axis=-1)


def bbox_from_mask(mask: np.ndarray, margin: int = 5) -> np.ndarray:
    ys, xs = np.where(mask)
    if ys.size == 0 or xs.size == 0:
        raise ValueError("cannot prompt SAM from an empty DIAS mask")
    y0 = max(int(ys.min()) - margin, 0)
    y1 = min(int(ys.max()) + margin, mask.shape[0] - 1)
    x0 = max(int(xs.min()) - margin, 0)
    x1 = min(int(xs.max()) + margin, mask.shape[1] - 1)
    return np.asarray([x0, y0, x1, y1], dtype=np.float32)


def dice(pred: np.ndarray, target: np.ndarray) -> float:
    pred = pred.astype(bool)
    target = target.astype(bool)
    denom = int(pred.sum() + target.sum())
    if denom == 0:
        return 1.0
    return float(2.0 * np.logical_and(pred, target).sum() / denom)


def cldice(pred: np.ndarray, target: np.ndarray) -> float:
    pred = pred.astype(bool)
    target = target.astype(bool)
    sp = morphology.skeletonize(pred)
    st = morphology.skeletonize(target)
    if not sp.any() and not st.any():
        return 1.0
    if not sp.any() or not st.any():
        return 0.0
    tprec = float(np.logical_and(sp, target).sum() / max(int(sp.sum()), 1))
    tsens = float(np.logical_and(st, pred).sum() / max(int(st.sum()), 1))
    if tprec + tsens == 0.0:
        return 0.0
    return float(2.0 * tprec * tsens / (tprec + tsens))


def component_count(mask: np.ndarray) -> int:
    return int(measure.label(mask.astype(bool), connectivity=2).max())


def build_predictor(checkpoint: Path, device: str) -> SamPredictor:
    model = sam_model_registry["vit_b"](checkpoint=str(checkpoint))
    model.to(device=device)
    model.eval()
    return SamPredictor(model)


def predict_mask(predictor: SamPredictor, image_rgb: np.ndarray, box: np.ndarray) -> tuple[np.ndarray, float]:
    predictor.set_image(image_rgb)
    masks, scores, _ = predictor.predict(box=box[None, :], multimask_output=True)
    best = int(np.argmax(scores))
    return masks[best].astype(bool), float(scores[best])


def save_mask_png(path: Path, mask: np.ndarray) -> None:
    Image.fromarray(mask.astype(np.uint8) * 255).save(path)


def save_overlay(path: Path, gray: np.ndarray, target: np.ndarray, pred: np.ndarray) -> None:
    rgb = to_rgb(gray).astype(np.float32)
    target_only = np.logical_and(target, ~pred)
    pred_only = np.logical_and(pred, ~target)
    overlap = np.logical_and(target, pred)
    rgb[target_only] = 0.55 * rgb[target_only] + np.asarray([0, 210, 0], dtype=np.float32) * 0.45
    rgb[pred_only] = 0.55 * rgb[pred_only] + np.asarray([220, 0, 0], dtype=np.float32) * 0.45
    rgb[overlap] = 0.45 * rgb[overlap] + np.asarray([230, 210, 0], dtype=np.float32) * 0.55
    Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)).save(path)


def write_preview_panel(path: Path, overlay_paths: list[Path]) -> None:
    images = [Image.open(p).convert("RGB") for p in overlay_paths]
    if not images:
        return
    thumb_w = 260
    resized = []
    for img in images:
        scale = thumb_w / img.width
        resized.append(img.resize((thumb_w, int(round(img.height * scale)))))
    width = thumb_w * 3
    height = max(img.height for img in resized[:3]) + max(img.height for img in resized[3:])
    panel = Image.new("RGB", (width, height), "white")
    for idx, img in enumerate(resized):
        x = (idx % 3) * thumb_w
        y = 0 if idx < 3 else max(im.height for im in resized[:3])
        panel.paste(img, (x, y))
    panel.save(path)


def mean_metric(rows: list[dict[str, Any]], frame_indices: list[int], key: str) -> float:
    selected = [r[key] for r in rows if int(r["frame_index"]) in set(frame_indices)]
    if not selected:
        raise ValueError(f"empty frame subset for {key}: {frame_indices}")
    return float(np.mean(selected))


def summarize_subset(
    rows: list[dict[str, Any]],
    family: str,
    severity: int,
    label: str,
    frame_indices: list[int],
    family_reference: dict[str, float] | None,
) -> dict[str, Any]:
    mean_dice = mean_metric(rows, frame_indices, "dice")
    mean_cldice = mean_metric(rows, frame_indices, "cldice")
    summary = {
        "family": family,
        "severity": severity,
        "subset_label": label,
        "frame_indices": frame_indices,
        "retained_frame_count": len(frame_indices),
        "mean_dice": mean_dice,
        "mean_cldice": mean_cldice,
        "min_dice": float(np.min([r["dice"] for r in rows if int(r["frame_index"]) in set(frame_indices)])),
        "min_cldice": float(np.min([r["cldice"] for r in rows if int(r["frame_index"]) in set(frame_indices)])),
    }
    if family_reference is None:
        summary["dice_delta_vs_family_severity0"] = 0.0
        summary["cldice_delta_vs_family_severity0"] = 0.0
    else:
        summary["dice_delta_vs_family_severity0"] = float(mean_dice - family_reference["mean_dice"])
        summary["cldice_delta_vs_family_severity0"] = float(mean_cldice - family_reference["mean_cldice"])
    return summary


def phase_label(frame_index: int, frame_count: int) -> str:
    third = frame_count / 3.0
    if frame_index < third:
        return "early"
    if frame_index < 2.0 * third:
        return "middle"
    return "late"


def analog_definitions(rows: list[dict[str, Any]]) -> dict[str, list[tuple[int, str, list[int]]]]:
    all_indices = [int(r["frame_index"]) for r in rows]
    even_stride = all_indices[::2]
    stride_three = all_indices[::3]
    means = {int(r["frame_index"]): float(r["intensity_mean"]) for r in rows}
    lowest_intensity = [min(means, key=means.get)]
    edge_half = [idx for idx in all_indices if idx in all_indices[:2] or idx in all_indices[-2:]]
    return {
        "frame_thinning": [
            (0, "all_frames", all_indices),
            (1, "stride_2_frames", even_stride),
            (2, "stride_3_frames", stride_three),
        ],
        "contrast_phase": [
            (0, "all_frames", all_indices),
            (1, "early_late_edge_frames", edge_half),
            (2, "lowest_intensity_frame", lowest_intensity),
        ],
    }


def choose_devices(requested: str) -> list[str]:
    if requested != "auto":
        return [requested]
    devices = []
    if torch.backends.mps.is_available():
        devices.append("mps")
    if torch.cuda.is_available():
        devices.append("cuda")
    devices.append("cpu")
    return devices


def run_once(args: argparse.Namespace, device: str) -> dict[str, Any]:
    workspace_root = args.workspace_root.resolve()
    manifest = load_json(args.manifest)
    sample = manifest["selected_sample"]
    label_path = resolve_path(workspace_root, sample["label_record"]["extracted_path"])
    frame_records = sorted(sample["frame_records"], key=lambda r: int(r["frame_index"]))
    frame_paths = [resolve_path(workspace_root, r["extracted_path"]) for r in frame_records]
    missing = [str(p) for p in [label_path, *frame_paths, args.checkpoint] if not p.exists()]
    if missing:
        raise FileNotFoundError(f"missing required inputs: {missing}")

    expected_sha = args.checkpoint_sha256
    actual_sha = sha256_file(args.checkpoint)
    if expected_sha and actual_sha != expected_sha:
        raise ValueError(f"checkpoint sha mismatch: expected {expected_sha}, got {actual_sha}")

    target = load_gray(label_path) > 0
    box = bbox_from_mask(target)
    target_area = int(target.sum())
    target_components = component_count(target)
    predictor = build_predictor(args.checkpoint, device)
    args.out.mkdir(parents=True, exist_ok=True)
    predictions_dir = args.out / "predictions"
    overlays_dir = args.out / "overlays"
    predictions_dir.mkdir(parents=True, exist_ok=True)
    overlays_dir.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, Any]] = []
    overlay_paths: list[Path] = []
    for record, frame_path in zip(frame_records, frame_paths):
        frame_index = int(record["frame_index"])
        gray = load_gray(frame_path)
        image_rgb = to_rgb(gray)
        pred, sam_score = predict_mask(predictor, image_rgb, box)
        pred_path = predictions_dir / f"s40_frame_{frame_index:02d}_mask.npy"
        pred_png_path = predictions_dir / f"s40_frame_{frame_index:02d}_mask.png"
        overlay_path = overlays_dir / f"s40_frame_{frame_index:02d}_overlay.png"
        np.save(pred_path, pred)
        save_mask_png(pred_png_path, pred)
        save_overlay(overlay_path, gray, target, pred)
        overlay_paths.append(overlay_path)
        pred_area = int(pred.sum())
        pred_components = component_count(pred)
        rows.append(
            {
                "sequence_id": sample["sequence_id"],
                "split": sample["split"],
                "frame_index": frame_index,
                "phase_label": phase_label(frame_index, len(frame_records)),
                "frame_path": str(frame_path.relative_to(workspace_root)),
                "prediction_path": str(pred_path.relative_to(args.out)),
                "prediction_png_path": str(pred_png_path.relative_to(args.out)),
                "overlay_path": str(overlay_path.relative_to(args.out)),
                "intensity_mean": float(np.mean(gray)),
                "intensity_std": float(np.std(gray)),
                "sam_score": sam_score,
                "dice": dice(pred, target),
                "cldice": cldice(pred, target),
                "pred_area_pixels": pred_area,
                "gt_area_pixels": target_area,
                "area_ratio": float(pred_area / max(target_area, 1)),
                "pred_component_count": pred_components,
                "gt_component_count": target_components,
                "component_count_ratio": float(pred_components / max(target_components, 1)),
            }
        )

    with (args.out / "per_frame_metrics.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    write_json(args.out / "per_frame_metrics.json", {"rows": rows})
    write_preview_panel(args.out / "dias_s40_sam_overlay_panel.png", overlay_paths)

    analog_rows: list[dict[str, Any]] = []
    for family, defs in analog_definitions(rows).items():
        reference = None
        for severity, label, frame_indices in defs:
            summary = summarize_subset(rows, family, severity, label, frame_indices, reference)
            if severity == 0:
                reference = {"mean_dice": summary["mean_dice"], "mean_cldice": summary["mean_cldice"]}
                summary["dice_delta_vs_family_severity0"] = 0.0
                summary["cldice_delta_vs_family_severity0"] = 0.0
            analog_rows.append(summary)

    with (args.out / "analog_summary.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(analog_rows[0].keys()))
        writer.writeheader()
        writer.writerows(analog_rows)
    write_json(args.out / "analog_summary.json", {"rows": analog_rows})

    frame_dice = [float(r["dice"]) for r in rows]
    frame_cldice = [float(r["cldice"]) for r in rows]
    summary_by_key = {(r["family"], int(r["severity"])): r for r in analog_rows}
    metrics = {
        **BASELINE_METRICS,
        "dias_sam_frame_count": float(len(rows)),
        "dias_sam_label_nonzero_pixels": float(target_area),
        "dias_sam_prompt_bbox_area_pixels": float((box[2] - box[0] + 1) * (box[3] - box[1] + 1)),
        "dias_sam_all_frame_mean_dice": float(np.mean(frame_dice)),
        "dias_sam_all_frame_mean_cldice": float(np.mean(frame_cldice)),
        "dias_sam_min_frame_dice": float(np.min(frame_dice)),
        "dias_sam_min_frame_cldice": float(np.min(frame_cldice)),
        "dias_sam_prediction_nonempty_rate": float(np.mean([r["pred_area_pixels"] > 0 for r in rows])),
        "dias_sam_finite_metric_check": 1.0,
    }
    for family in ["frame_thinning", "contrast_phase"]:
        for severity in [0, 1, 2]:
            row = summary_by_key[(family, severity)]
            prefix = f"dias_sam_{family}_severity{severity}"
            metrics[f"{prefix}_mean_dice"] = float(row["mean_dice"])
            metrics[f"{prefix}_mean_cldice"] = float(row["mean_cldice"])
            metrics[f"{prefix}_dice_delta_vs_severity0"] = float(row["dice_delta_vs_family_severity0"])
            metrics[f"{prefix}_cldice_delta_vs_severity0"] = float(row["cldice_delta_vs_family_severity0"])

    metric_values = [v for v in metrics.values() if isinstance(v, (float, int))]
    if not all(np.isfinite(metric_values)):
        metrics["dias_sam_finite_metric_check"] = 0.0
        raise ValueError("nonfinite metric detected")

    write_json(args.out / "metrics_summary.json", metrics)
    write_json(
        args.out / "manifest.json",
        {
            "run_id": RUN_ID,
            "parent_run_id": manifest["run_id"],
            "dataset": "DIAS",
            "sequence_id": sample["sequence_id"],
            "split": sample["split"],
            "frame_count": len(rows),
            "model": {
                "model_id": "sam_vit_b",
                "checkpoint_path": str(args.checkpoint),
                "checkpoint_sha256": actual_sha,
                "prompt_source": "DIAS sequence-level mask bbox; smoke-test oracle prompt, not a deployable prompt source",
                "prompt_box_xyxy": [float(x) for x in box.tolist()],
            },
            "device": device,
            "analog_definitions": {
                family: [
                    {"severity": sev, "subset_label": label, "frame_indices": frames}
                    for sev, label, frames in defs
                ]
                for family, defs in analog_definitions(rows).items()
            },
            "source_manifest": str(args.manifest),
            "outputs": {
                "per_frame_metrics_csv": "per_frame_metrics.csv",
                "per_frame_metrics_json": "per_frame_metrics.json",
                "analog_summary_csv": "analog_summary.csv",
                "analog_summary_json": "analog_summary.json",
                "metrics_summary": "metrics_summary.json",
                "overlay_panel": "dias_s40_sam_overlay_panel.png",
            },
            "claim_boundary": (
                "Frozen-model real-data smoke only. This supports real DIAS harness feasibility "
                "and analog metric extraction, not construct validity or clinical accuracy."
            ),
        },
    )
    write_run_notes(args.out, args, device, actual_sha, metrics, rows, analog_rows)
    return {"metrics": metrics, "rows": rows, "analog_rows": analog_rows, "checkpoint_sha256": actual_sha}


def write_run_notes(
    out_dir: Path,
    args: argparse.Namespace,
    device: str,
    checkpoint_sha256: str,
    metrics: dict[str, float],
    rows: list[dict[str, Any]],
    analog_rows: list[dict[str, Any]],
) -> None:
    command = " ".join(sys.argv)
    run_md = f"""# RUN

## Identity

- run_id: `{RUN_ID}`
- parent_run_id: `run-angiostress-s2-real-dsa-loader-smoke`
- command: `{command}`
- device: `{device}`
- checkpoint_sha256: `{checkpoint_sha256}`

## Inputs

- DIAS manifest: `{args.manifest}`
- SAM checkpoint: `{args.checkpoint}`
- Frame count: `{len(rows)}`

## Method

Frozen SAM ViT-B is prompted with the DIAS sequence-level label bounding box and evaluated on each extracted `s40` frame. Frame-thinning and contrast-phase analogs are summarized from deterministic frame subsets after per-frame predictions are computed.

## Claim Boundary

This is a real-data harness smoke only. It does not estimate construct validity, model ordering, or clinical accuracy.
"""
    validation_md = f"""# VALIDATION

## Checks

- outputs_exist: true
- finite_metric_check: `{metrics["dias_sam_finite_metric_check"]}`
- frame_count: `{metrics["dias_sam_frame_count"]}`
- prediction_nonempty_rate: `{metrics["dias_sam_prediction_nonempty_rate"]}`
- all_frame_mean_dice: `{metrics["dias_sam_all_frame_mean_dice"]:.6f}`
- all_frame_mean_cldice: `{metrics["dias_sam_all_frame_mean_cldice"]:.6f}`

## Analog Rows

{json.dumps(analog_rows, indent=2)}

## Caveats

- DIAS provides a sequence-level mask here, so per-frame phase summaries are approximate.
- The SAM box prompt is derived from the label and is suitable for a harness smoke, not a deployable model setting.
- Device-overlay analogs remain deferred because CathAction data are not locally loaded.
"""
    (out_dir.parent / "RUN.md").write_text(run_md)
    (out_dir.parent / "VALIDATION.md").write_text(validation_md)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--workspace-root", type=Path, default=Path.cwd())
    parser.add_argument("--checkpoint-sha256", default="ec2df62732614e57411cdcf32a23ffdf28910380d03139ee0f4fcbe91eb8c912")
    parser.add_argument("--device", default="auto", choices=["auto", "cpu", "mps", "cuda"])
    args = parser.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    errors = []
    for device in choose_devices(args.device):
        try:
            result = run_once(args, device)
            write_json(
                args.out / "environment.json",
                {
                    "python": sys.version.split()[0],
                    "platform": platform.platform(),
                    "torch": torch.__version__,
                    "device": device,
                },
            )
            print(
                json.dumps(
                    {
                        "run_id": RUN_ID,
                        "device": device,
                        "rows": len(result["rows"]),
                        "all_frame_mean_dice": result["metrics"]["dias_sam_all_frame_mean_dice"],
                        "all_frame_mean_cldice": result["metrics"]["dias_sam_all_frame_mean_cldice"],
                        "metrics": str((args.out / "metrics_summary.json").resolve()),
                    },
                    indent=2,
                    sort_keys=True,
                )
            )
            return 0
        except Exception as exc:
            errors.append({"device": device, "error": type(exc).__name__, "message": str(exc)})
            if device == choose_devices(args.device)[-1]:
                write_json(args.out / "BLOCKER.json", {"run_id": RUN_ID, "errors": errors})
                raise
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
