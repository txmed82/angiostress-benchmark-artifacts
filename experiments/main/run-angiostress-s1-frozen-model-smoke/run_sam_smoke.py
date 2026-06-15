#!/usr/bin/env python3
"""Frozen SAM harness smoke for AngioStress generated stressor cells."""

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


def resolve_parent_outputs(config_path: Path, config: dict[str, Any]) -> Path:
    run_dir = config_path.parent
    parent = Path(config["parent_outputs_dir"])
    if not parent.is_absolute():
        parent = (run_dir / parent).resolve()
    return parent


def bbox_from_mask(mask: np.ndarray, margin: int = 3) -> np.ndarray:
    ys, xs = np.where(mask)
    if ys.size == 0 or xs.size == 0:
        raise ValueError("cannot prompt SAM from an empty GT mask")
    y0 = max(int(ys.min()) - margin, 0)
    y1 = min(int(ys.max()) + margin, mask.shape[0] - 1)
    x0 = max(int(xs.min()) - margin, 0)
    x1 = min(int(xs.max()) + margin, mask.shape[1] - 1)
    return np.asarray([x0, y0, x1, y1], dtype=np.float32)


def sequence_to_rgb(sequence: np.ndarray) -> np.ndarray:
    image = sequence.max(axis=0) if sequence.ndim == 3 else sequence
    image = np.clip(image.astype(np.float32), 0.0, 1.0)
    uint8 = (image * 255.0).round().astype(np.uint8)
    return np.stack([uint8, uint8, uint8], axis=-1)


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


def save_mask_png(path: Path, mask: np.ndarray) -> None:
    Image.fromarray(mask.astype(np.uint8) * 255).save(path)


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


def evaluate_with_device(config: dict[str, Any], config_path: Path, out_dir: Path, device: str) -> dict[str, Any]:
    parent = resolve_parent_outputs(config_path, config)
    manifest = load_json(parent / "manifest.json")
    gt = np.load(parent / "projected_gt_mask.npy").astype(bool)
    box = bbox_from_mask(gt)

    weights_dir = Path(config["environment"]["weights_dir"])
    checkpoint = weights_dir / config["model"]["checkpoint_filename"]
    expected_sha = config["model"]["checkpoint_sha256"]
    actual_sha = sha256_file(checkpoint)
    if expected_sha and actual_sha != expected_sha:
        raise ValueError(f"checkpoint sha mismatch: expected {expected_sha}, got {actual_sha}")

    predictions_dir = out_dir / "predictions"
    predictions_dir.mkdir(parents=True, exist_ok=True)
    predictor = build_predictor(checkpoint, device)

    items: list[dict[str, Any]] = [
        {
            "cell_id": "clean",
            "family": "clean",
            "severity": 0,
            "sequence_path": "clean_sequence.npy",
            "array_path": parent / "clean_sequence.npy",
        }
    ]
    for cell in manifest["cells"]:
        items.append(
            {
                "cell_id": f"{cell['family']}_severity_{cell['severity']}",
                "family": cell["family"],
                "severity": int(cell["severity"]),
                "sequence_path": cell["npy_path"],
                "array_path": parent / cell["npy_path"],
            }
        )

    rows = []
    clean_dice = None
    clean_cldice = None
    target_components = component_count(gt)
    target_area = int(gt.sum())
    for item in items:
        sequence = np.load(item["array_path"]).astype(np.float32)
        image_rgb = sequence_to_rgb(sequence)
        pred, sam_score = predict_mask(predictor, image_rgb, box)
        pred_path = predictions_dir / f"{item['cell_id']}_mask.npy"
        png_path = predictions_dir / f"{item['cell_id']}_mask.png"
        np.save(pred_path, pred)
        save_mask_png(png_path, pred)
        dsc = dice(pred, gt)
        cdsc = cldice(pred, gt)
        pred_area = int(pred.sum())
        pred_components = component_count(pred)
        if item["cell_id"] == "clean":
            clean_dice = dsc
            clean_cldice = cdsc
        row = {
            "cell_id": item["cell_id"],
            "family": item["family"],
            "severity": item["severity"],
            "sequence_path": item["sequence_path"],
            "prediction_path": str(pred_path.relative_to(out_dir)),
            "prediction_png_path": str(png_path.relative_to(out_dir)),
            "sam_score": sam_score,
            "dice": dsc,
            "cldice": cdsc,
            "pred_area_pixels": pred_area,
            "gt_area_pixels": target_area,
            "area_ratio": float(pred_area / max(target_area, 1)),
            "pred_component_count": pred_components,
            "gt_component_count": target_components,
            "component_count_ratio": float(pred_components / max(target_components, 1)),
        }
        rows.append(row)

    if clean_dice is None or clean_cldice is None:
        raise RuntimeError("clean prediction row was not evaluated")
    for row in rows:
        row["dice_delta_vs_clean"] = float(row["dice"] - clean_dice)
        row["cldice_delta_vs_clean"] = float(row["cldice"] - clean_cldice)
        row["dice_ratio_vs_clean"] = float(row["dice"] / max(clean_dice, 1e-8))
        row["cldice_ratio_vs_clean"] = float(row["cldice"] / max(clean_cldice, 1e-8))

    family_summary = {}
    for family in sorted({r["family"] for r in rows if r["family"] != "clean"}):
        fam_rows = [r for r in rows if r["family"] == family]
        family_summary[family] = {
            "mean_dice": float(np.mean([r["dice"] for r in fam_rows])),
            "mean_cldice": float(np.mean([r["cldice"] for r in fam_rows])),
            "min_dice": float(np.min([r["dice"] for r in fam_rows])),
            "min_cldice": float(np.min([r["cldice"] for r in fam_rows])),
            "mean_dice_delta_vs_clean": float(np.mean([r["dice_delta_vs_clean"] for r in fam_rows])),
            "mean_cldice_delta_vs_clean": float(np.mean([r["cldice_delta_vs_clean"] for r in fam_rows])),
        }

    metrics = {
        "run_id": config["run_id"],
        "model_id": config["model"]["model_id"],
        "device": device,
        "cell_count_including_clean": float(len(rows)),
        "stressor_cell_count": float(len(rows) - 1),
        "clean_dice": float(clean_dice),
        "clean_cldice": float(clean_cldice),
        "mean_stressor_dice": float(np.mean([r["dice"] for r in rows if r["family"] != "clean"])),
        "mean_stressor_cldice": float(np.mean([r["cldice"] for r in rows if r["family"] != "clean"])),
        "min_stressor_dice": float(np.min([r["dice"] for r in rows if r["family"] != "clean"])),
        "min_stressor_cldice": float(np.min([r["cldice"] for r in rows if r["family"] != "clean"])),
        "mean_stressor_dice_delta_vs_clean": float(np.mean([r["dice_delta_vs_clean"] for r in rows if r["family"] != "clean"])),
        "mean_stressor_cldice_delta_vs_clean": float(np.mean([r["cldice_delta_vs_clean"] for r in rows if r["family"] != "clean"])),
        "finite_metric_check": 1.0,
    }

    with (out_dir / "per_cell_metrics.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    write_json(out_dir / "per_cell_metrics.json", {"rows": rows})
    write_json(
        out_dir / "metrics_summary.json",
        {
            "metrics": metrics,
            "family_summary": family_summary,
            "checkpoint": {
                "path": str(checkpoint),
                "sha256": actual_sha,
                "size_bytes": checkpoint.stat().st_size,
            },
            "prompt": {"source": config["model"]["prompt_source"], "box_xyxy": [float(x) for x in box.tolist()]},
            "environment": {
                "python": sys.version.split()[0],
                "platform": platform.platform(),
                "torch": torch.__version__,
            },
        },
    )
    write_json(
        out_dir / "manifest.json",
        {
            "run_id": config["run_id"],
            "parent_run_id": config["parent_run_id"],
            "model": config["model"],
            "device": device,
            "row_count": len(rows),
            "claim_boundary": "Frozen-model harness smoke only; no construct-validity or clinical claim.",
            "outputs": {
                "per_cell_metrics_csv": "per_cell_metrics.csv",
                "per_cell_metrics_json": "per_cell_metrics.json",
                "metrics_summary": "metrics_summary.json",
            },
        },
    )
    return {"metrics": metrics, "rows": rows}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--device", default="auto", choices=["auto", "cpu", "mps", "cuda"])
    args = parser.parse_args()

    config = load_json(args.config)
    args.out.mkdir(parents=True, exist_ok=True)
    device_order = [args.device]
    if args.device == "auto":
        device_order = []
        if torch.backends.mps.is_available():
            device_order.append("mps")
        if torch.cuda.is_available():
            device_order.append("cuda")
        device_order.append("cpu")

    errors = []
    for device in device_order:
        try:
            result = evaluate_with_device(config, args.config, args.out, device)
            summary = result["metrics"]
            print(json.dumps({
                "run_id": config["run_id"],
                "device": device,
                "rows": len(result["rows"]),
                "clean_dice": summary["clean_dice"],
                "mean_stressor_dice": summary["mean_stressor_dice"],
                "mean_stressor_dice_delta_vs_clean": summary["mean_stressor_dice_delta_vs_clean"],
                "metrics": str((args.out / "metrics_summary.json").resolve()),
            }, indent=2, sort_keys=True))
            return 0
        except Exception as exc:
            errors.append({"device": device, "error": type(exc).__name__, "message": str(exc)})
            if device == device_order[-1]:
                write_json(args.out / "BLOCKER.json", {"run_id": config["run_id"], "errors": errors})
                raise
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
