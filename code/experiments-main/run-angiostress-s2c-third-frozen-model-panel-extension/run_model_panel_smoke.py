#!/usr/bin/env python3
"""Frozen three-model panel smoke for AngioStress synthetic and DIAS surfaces."""

from __future__ import annotations

import argparse
import csv
import gc
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


RUN_ID = "run-angiostress-s2c-third-frozen-model-panel-extension"
BASELINE_METRICS = {
    "topcow_resencm_one_case_mean_dice": 0.6984658547796687,
    "topcow_resencm_one_case_mean_cldice": 0.6285484218960072,
    "topcow_resencm_one_case_graph_ready_rate": 1.0,
    "topcow_gt_sanity_mean_dice": 1.0,
    "topcow_gt_sanity_mean_cldice": 1.0,
    "topcow_gt_sanity_graph_ready_rate": 1.0,
}


MODEL_PANEL = [
    {
        "model_id": "sam_vit_b",
        "display_name": "SAM ViT-B",
        "model_type": "vit_b",
        "checkpoint": "/Users/colin/DeepScientist/quests/010/tmp/angiostress-s1-weights/sam_vit_b_01ec64.pth",
        "checkpoint_sha256": "ec2df62732614e57411cdcf32a23ffdf28910380d03139ee0f4fcbe91eb8c912",
        "source": "Meta Segment Anything ViT-B checkpoint used in S1/S3.",
        "checkpoint_note": "Original checkpoint loads directly on this host.",
    },
    {
        "model_id": "medsam_vit_b",
        "display_name": "MedSAM ViT-B",
        "model_type": "vit_b",
        "checkpoint": "/Users/colin/DeepScientist/quests/010/tmp/angiostress-s2b-weights/medsam/medsam_vit_b.cpu.pth",
        "checkpoint_sha256": "ec970b350c62fed9a81855ae4c4532bb0421e0edaa7b7e944a4f7951934753cb",
        "source": "MedSAM repository README checkpoint folder; official file was CPU-mapped locally for non-CUDA loading.",
        "checkpoint_note": "CPU-mapped copy of official CUDA-serialized checkpoint; original SHA256 34b34b78c1d18cb8c6bf84cf9c00e135d6d6c965699f3c0e31ef1bc9dcb5be74.",
    },
    {
        "model_id": "sam_vit_l",
        "display_name": "SAM ViT-L",
        "model_type": "vit_l",
        "checkpoint": "/Users/colin/DeepScientist/quests/010/tmp/angiostress-s2c-weights/sam/sam_vit_l_0b3195.pth",
        "checkpoint_sha256": "3adcc4315b642a4d2101128f611684e8734c41232a17c648ed1693702a49a622",
        "source": "Meta Segment Anything official README ViT-L checkpoint URL.",
        "checkpoint_note": "Official checkpoint loaded on MPS in one-frame S2c candidate smoke.",
    },
]


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty CSV: {path}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def resolve_path(workspace_root: Path, value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    return (workspace_root / path).resolve()


def bbox_from_mask(mask: np.ndarray, margin: int) -> np.ndarray:
    ys, xs = np.where(mask)
    if ys.size == 0 or xs.size == 0:
        raise ValueError("cannot prompt from an empty mask")
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


def gray_to_rgb(gray: np.ndarray) -> np.ndarray:
    if gray.dtype != np.uint8:
        gray = np.clip(gray, 0, 255).astype(np.uint8)
    return np.stack([gray, gray, gray], axis=-1)


def load_gray(path: Path) -> np.ndarray:
    return np.asarray(Image.open(path).convert("L"))


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


def save_overlay(path: Path, gray: np.ndarray, target: np.ndarray, pred: np.ndarray) -> None:
    rgb = gray_to_rgb(gray).astype(np.float32)
    target_only = np.logical_and(target, ~pred)
    pred_only = np.logical_and(pred, ~target)
    overlap = np.logical_and(target, pred)
    rgb[target_only] = 0.55 * rgb[target_only] + np.asarray([0, 210, 0], dtype=np.float32) * 0.45
    rgb[pred_only] = 0.55 * rgb[pred_only] + np.asarray([220, 0, 0], dtype=np.float32) * 0.45
    rgb[overlap] = 0.45 * rgb[overlap] + np.asarray([230, 210, 0], dtype=np.float32) * 0.55
    Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)).save(path)


def build_predictor(model: dict[str, Any], device: str) -> tuple[SamPredictor, str]:
    checkpoint = Path(model["checkpoint"])
    if not checkpoint.exists():
        raise FileNotFoundError(f"missing checkpoint for {model['model_id']}: {checkpoint}")
    actual_sha = sha256_file(checkpoint)
    expected_sha = model.get("checkpoint_sha256")
    if expected_sha and actual_sha != expected_sha:
        raise ValueError(f"{model['model_id']} checkpoint sha mismatch: expected {expected_sha}, got {actual_sha}")
    model_type = model.get("model_type", "vit_b")
    sam = sam_model_registry[model_type](checkpoint=str(checkpoint))
    sam.to(device=device)
    sam.eval()
    return SamPredictor(sam), actual_sha


def predict_mask(predictor: SamPredictor, image_rgb: np.ndarray, box: np.ndarray) -> tuple[np.ndarray, float]:
    predictor.set_image(image_rgb)
    masks, scores, _ = predictor.predict(box=box[None, :], multimask_output=True)
    best = int(np.argmax(scores))
    return masks[best].astype(bool), float(scores[best])


def synthetic_items(workspace_root: Path, limit: int) -> tuple[list[dict[str, Any]], np.ndarray, np.ndarray]:
    parent = workspace_root / "experiments/main/run-angiostress-s0s1-renderer-smoke/outputs"
    manifest = read_json(parent / "manifest.json")
    gt = np.load(parent / "projected_gt_mask.npy").astype(bool)
    box = bbox_from_mask(gt, margin=3)
    items = [
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
    if limit > 0:
        clean = [item for item in items if item["cell_id"] == "clean"]
        rest = [item for item in items if item["cell_id"] != "clean"][: max(limit - 1, 0)]
        items = clean + rest
    missing = [str(item["array_path"]) for item in items if not item["array_path"].exists()]
    if missing:
        raise FileNotFoundError(f"missing synthetic arrays: {missing}")
    return items, gt, box


def dias_items(workspace_root: Path, limit: int) -> tuple[list[dict[str, Any]], np.ndarray, np.ndarray, dict[str, Any]]:
    manifest = read_json(
        workspace_root / "experiments/main/run-angiostress-s2-real-dsa-loader-smoke/outputs/real_dsa_loader_manifest.json"
    )
    sample = manifest["selected_sample"]
    label_path = resolve_path(workspace_root, sample["label_record"]["extracted_path"])
    target = load_gray(label_path) > 0
    box = bbox_from_mask(target, margin=5)
    frame_records = sorted(sample["frame_records"], key=lambda r: int(r["frame_index"]))
    if limit > 0:
        frame_records = frame_records[:limit]
    items = []
    for record in frame_records:
        frame_path = resolve_path(workspace_root, record["extracted_path"])
        if not frame_path.exists():
            raise FileNotFoundError(f"missing DIAS frame: {frame_path}")
        items.append(
            {
                "sequence_id": sample["sequence_id"],
                "split": sample["split"],
                "frame_index": int(record["frame_index"]),
                "frame_path": frame_path,
            }
        )
    return items, target, box, sample


def phase_label(frame_index: int, frame_count: int) -> str:
    third = frame_count / 3.0
    if frame_index < third:
        return "early"
    if frame_index < 2.0 * third:
        return "middle"
    return "late"


def mean_metric(rows: list[dict[str, Any]], frame_indices: list[int], key: str) -> float:
    selected = [float(r[key]) for r in rows if int(r["frame_index"]) in set(frame_indices)]
    if not selected:
        raise ValueError(f"empty frame subset for {key}: {frame_indices}")
    return float(np.mean(selected))


def summarize_dias_subset(
    rows: list[dict[str, Any]],
    family: str,
    severity: int,
    subset_label: str,
    frame_indices: list[int],
    reference: dict[str, float] | None,
) -> dict[str, Any]:
    mean_dice = mean_metric(rows, frame_indices, "dice")
    mean_cldice = mean_metric(rows, frame_indices, "cldice")
    selected = [r for r in rows if int(r["frame_index"]) in set(frame_indices)]
    summary = {
        "model_id": rows[0]["model_id"],
        "family": family,
        "severity": severity,
        "subset_label": subset_label,
        "frame_indices": frame_indices,
        "retained_frame_count": len(frame_indices),
        "mean_dice": mean_dice,
        "mean_cldice": mean_cldice,
        "min_dice": float(np.min([r["dice"] for r in selected])),
        "min_cldice": float(np.min([r["cldice"] for r in selected])),
    }
    if reference is None:
        summary["dice_delta_vs_family_severity0"] = 0.0
        summary["cldice_delta_vs_family_severity0"] = 0.0
    else:
        summary["dice_delta_vs_family_severity0"] = float(mean_dice - reference["mean_dice"])
        summary["cldice_delta_vs_family_severity0"] = float(mean_cldice - reference["mean_cldice"])
    return summary


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


def evaluate_synthetic_model(
    predictor: SamPredictor,
    model: dict[str, Any],
    items: list[dict[str, Any]],
    gt: np.ndarray,
    box: np.ndarray,
    out_dir: Path,
) -> list[dict[str, Any]]:
    pred_dir = out_dir / "synthetic_predictions" / model["model_id"]
    pred_dir.mkdir(parents=True, exist_ok=True)
    target_area = int(gt.sum())
    target_components = component_count(gt)
    rows = []
    clean_dice = None
    clean_cldice = None
    for item in items:
        sequence = np.load(item["array_path"]).astype(np.float32)
        pred, score = predict_mask(predictor, sequence_to_rgb(sequence), box)
        pred_path = pred_dir / f"{item['cell_id']}_mask.npy"
        pred_png_path = pred_dir / f"{item['cell_id']}_mask.png"
        np.save(pred_path, pred)
        save_mask_png(pred_png_path, pred)
        dsc = dice(pred, gt)
        cdsc = cldice(pred, gt)
        if item["cell_id"] == "clean":
            clean_dice = dsc
            clean_cldice = cdsc
        pred_area = int(pred.sum())
        pred_components = component_count(pred)
        rows.append(
            {
                "model_id": model["model_id"],
                "surface": "synthetic_topcow_projection",
                "cell_id": item["cell_id"],
                "family": item["family"],
                "severity": item["severity"],
                "sequence_path": item["sequence_path"],
                "prediction_path": str(pred_path.relative_to(out_dir)),
                "prediction_png_path": str(pred_png_path.relative_to(out_dir)),
                "sam_score": score,
                "dice": dsc,
                "cldice": cdsc,
                "pred_area_pixels": pred_area,
                "gt_area_pixels": target_area,
                "area_ratio": float(pred_area / max(target_area, 1)),
                "pred_component_count": pred_components,
                "gt_component_count": target_components,
                "component_count_ratio": float(pred_components / max(target_components, 1)),
            }
        )
    if clean_dice is None or clean_cldice is None:
        raise RuntimeError("clean synthetic row was not evaluated")
    for row in rows:
        row["dice_delta_vs_clean"] = float(row["dice"] - clean_dice)
        row["cldice_delta_vs_clean"] = float(row["cldice"] - clean_cldice)
    return rows


def evaluate_dias_model(
    predictor: SamPredictor,
    model: dict[str, Any],
    items: list[dict[str, Any]],
    target: np.ndarray,
    box: np.ndarray,
    out_dir: Path,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    pred_dir = out_dir / "dias_predictions" / model["model_id"]
    overlay_dir = out_dir / "dias_overlays" / model["model_id"]
    pred_dir.mkdir(parents=True, exist_ok=True)
    overlay_dir.mkdir(parents=True, exist_ok=True)
    target_area = int(target.sum())
    target_components = component_count(target)
    rows = []
    for item in items:
        gray = load_gray(item["frame_path"])
        pred, score = predict_mask(predictor, gray_to_rgb(gray), box)
        frame_index = int(item["frame_index"])
        pred_path = pred_dir / f"s40_frame_{frame_index:02d}_mask.npy"
        pred_png_path = pred_dir / f"s40_frame_{frame_index:02d}_mask.png"
        overlay_path = overlay_dir / f"s40_frame_{frame_index:02d}_overlay.png"
        np.save(pred_path, pred)
        save_mask_png(pred_png_path, pred)
        save_overlay(overlay_path, gray, target, pred)
        pred_area = int(pred.sum())
        pred_components = component_count(pred)
        rows.append(
            {
                "model_id": model["model_id"],
                "surface": "dias_s40",
                "sequence_id": item["sequence_id"],
                "split": item["split"],
                "frame_index": frame_index,
                "phase_label": phase_label(frame_index, len(items)),
                "frame_path": str(item["frame_path"]),
                "prediction_path": str(pred_path.relative_to(out_dir)),
                "prediction_png_path": str(pred_png_path.relative_to(out_dir)),
                "overlay_path": str(overlay_path.relative_to(out_dir)),
                "intensity_mean": float(np.mean(gray)),
                "intensity_std": float(np.std(gray)),
                "sam_score": score,
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

    analog_rows = []
    for family, defs in analog_definitions(rows).items():
        reference = None
        for severity, subset_label, frame_indices in defs:
            summary = summarize_dias_subset(rows, family, severity, subset_label, frame_indices, reference)
            if severity == 0:
                reference = {"mean_dice": summary["mean_dice"], "mean_cldice": summary["mean_cldice"]}
                summary["dice_delta_vs_family_severity0"] = 0.0
                summary["cldice_delta_vs_family_severity0"] = 0.0
            analog_rows.append(summary)
    return rows, analog_rows


def summarize_synthetic(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    summaries = []
    for model_id in sorted({r["model_id"] for r in rows}):
        model_rows = [r for r in rows if r["model_id"] == model_id]
        clean = next(r for r in model_rows if r["family"] == "clean")
        for family in sorted({r["family"] for r in model_rows if r["family"] != "clean"}):
            family_rows = sorted([r for r in model_rows if r["family"] == family], key=lambda r: int(r["severity"]))
            reference = next((r for r in family_rows if int(r["severity"]) == 0), family_rows[0])
            for row in family_rows:
                summaries.append(
                    {
                        "model_id": model_id,
                        "family": family,
                        "severity": int(row["severity"]),
                        "mean_dice": float(row["dice"]),
                        "mean_cldice": float(row["cldice"]),
                        "dice_delta_vs_clean": float(row["dice"] - clean["dice"]),
                        "cldice_delta_vs_clean": float(row["cldice"] - clean["cldice"]),
                        "dice_delta_vs_family_severity0": float(row["dice"] - reference["dice"]),
                        "cldice_delta_vs_family_severity0": float(row["cldice"] - reference["cldice"]),
                    }
                )
    return summaries


def model_summary_rows(
    synthetic_rows: list[dict[str, Any]], dias_rows: list[dict[str, Any]], dias_analog_rows: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    rows = []
    for model_id in sorted({r["model_id"] for r in synthetic_rows}):
        syn = [r for r in synthetic_rows if r["model_id"] == model_id]
        dias = [r for r in dias_rows if r["model_id"] == model_id]
        analog = {(r["family"], int(r["severity"])): r for r in dias_analog_rows if r["model_id"] == model_id}
        clean = next(r for r in syn if r["family"] == "clean")
        stressed = [r for r in syn if r["family"] != "clean"]
        rows.append(
            {
                "model_id": model_id,
                "synthetic_clean_dice": float(clean["dice"]),
                "synthetic_clean_cldice": float(clean["cldice"]),
                "synthetic_mean_stressor_dice": float(np.mean([r["dice"] for r in stressed])),
                "synthetic_mean_stressor_cldice": float(np.mean([r["cldice"] for r in stressed])),
                "synthetic_min_stressor_dice": float(np.min([r["dice"] for r in stressed])),
                "synthetic_min_stressor_cldice": float(np.min([r["cldice"] for r in stressed])),
                "synthetic_mean_stressor_dice_delta_vs_clean": float(np.mean([r["dice_delta_vs_clean"] for r in stressed])),
                "dias_all_frame_mean_dice": float(np.mean([r["dice"] for r in dias])),
                "dias_all_frame_mean_cldice": float(np.mean([r["cldice"] for r in dias])),
                "dias_min_frame_dice": float(np.min([r["dice"] for r in dias])),
                "dias_min_frame_cldice": float(np.min([r["cldice"] for r in dias])),
                "dias_prediction_nonempty_rate": float(np.mean([r["pred_area_pixels"] > 0 for r in dias])),
                "dias_frame_thinning_severity2_dice_delta_vs_severity0": float(
                    analog[("frame_thinning", 2)]["dice_delta_vs_family_severity0"]
                ),
                "dias_contrast_phase_severity2_dice_delta_vs_severity0": float(
                    analog[("contrast_phase", 2)]["dice_delta_vs_family_severity0"]
                ),
            }
        )
    return rows


def ranking_rows(summary_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    ranking_metrics = [
        ("synthetic_mean_stressor_dice", "higher_is_better"),
        ("synthetic_mean_stressor_dice_delta_vs_clean", "higher_is_better"),
        ("dias_all_frame_mean_dice", "higher_is_better"),
        ("dias_frame_thinning_severity2_dice_delta_vs_severity0", "higher_is_better"),
        ("dias_contrast_phase_severity2_dice_delta_vs_severity0", "higher_is_better"),
    ]
    rows = []
    for metric, direction in ranking_metrics:
        reverse = direction == "higher_is_better"
        ordered = sorted(summary_rows, key=lambda r: float(r[metric]), reverse=reverse)
        for rank, row in enumerate(ordered, start=1):
            rows.append(
                {
                    "ranking_metric": metric,
                    "direction": direction,
                    "rank": rank,
                    "model_id": row["model_id"],
                    "value": float(row[metric]),
                }
            )
    return rows


def order_for_metric(summary_rows: list[dict[str, Any]], metric: str) -> list[str]:
    return [r["model_id"] for r in sorted(summary_rows, key=lambda r: float(r[metric]), reverse=True)]


def average_descending_ranks(values: list[float]) -> list[float]:
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


def spearman_rank(xs: list[float], ys: list[float]) -> float | None:
    if len(xs) < 3 or len(xs) != len(ys):
        return None
    xr = np.asarray(average_descending_ranks(xs), dtype=np.float64)
    yr = np.asarray(average_descending_ranks(ys), dtype=np.float64)
    if float(np.std(xr)) == 0.0 or float(np.std(yr)) == 0.0:
        return None
    return float(np.corrcoef(xr, yr)[0, 1])


def ordering_comparison(summary_rows: list[dict[str, Any]]) -> dict[str, Any]:
    synthetic_order = order_for_metric(summary_rows, "synthetic_mean_stressor_dice")
    dias_order = order_for_metric(summary_rows, "dias_all_frame_mean_dice")
    spearman = spearman_rank(
        [float(r["synthetic_mean_stressor_dice"]) for r in summary_rows],
        [float(r["dias_all_frame_mean_dice"]) for r in summary_rows],
    )
    return {
        "ranked_model_count": len(summary_rows),
        "synthetic_mean_stressor_dice_order": synthetic_order,
        "dias_all_frame_mean_dice_order": dias_order,
        "spearman_synthetic_mean_stressor_dice_vs_dias_mean_dice": spearman,
        "rank_correlation_status": (
            "smoke_rank_diagnostic_no_ci_n3_one_sequence"
            if spearman is not None
            else "not_estimated_for_construct_validity_insufficient_panel"
        ),
        "claim_boundary": (
            "Three-model ordering rows are a smoke diagnostic only and cannot support "
            "construct-validity claims or confidence intervals."
        ),
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


def evaluate_all(args: argparse.Namespace, device: str) -> dict[str, Any]:
    workspace_root = args.workspace_root.resolve()
    args.out.mkdir(parents=True, exist_ok=True)
    synthetic_inputs, synthetic_gt, synthetic_box = synthetic_items(workspace_root, args.max_synthetic_items)
    dias_inputs, dias_target, dias_box, dias_sample = dias_items(workspace_root, args.max_dias_frames)

    model_records = []
    synthetic_rows: list[dict[str, Any]] = []
    dias_rows: list[dict[str, Any]] = []
    dias_analog_rows: list[dict[str, Any]] = []
    for model in MODEL_PANEL:
        predictor, checkpoint_sha = build_predictor(model, device)
        model_records.append(
            {
                **{k: v for k, v in model.items() if k != "checkpoint"},
                "checkpoint_path": model["checkpoint"],
                "verified_checkpoint_sha256": checkpoint_sha,
            }
        )
        synthetic_rows.extend(evaluate_synthetic_model(predictor, model, synthetic_inputs, synthetic_gt, synthetic_box, args.out))
        model_dias_rows, model_analog_rows = evaluate_dias_model(predictor, model, dias_inputs, dias_target, dias_box, args.out)
        dias_rows.extend(model_dias_rows)
        dias_analog_rows.extend(model_analog_rows)
        del predictor
        gc.collect()
        if device == "mps":
            torch.mps.empty_cache()

    synthetic_summary = summarize_synthetic(synthetic_rows)
    summary_rows = model_summary_rows(synthetic_rows, dias_rows, dias_analog_rows)
    ranks = ranking_rows(summary_rows)
    order_compare = ordering_comparison(summary_rows)

    write_csv(args.out / "synthetic_per_cell_metrics.csv", synthetic_rows)
    write_json(args.out / "synthetic_per_cell_metrics.json", {"rows": synthetic_rows})
    write_csv(args.out / "synthetic_degradation_summary.csv", synthetic_summary)
    write_json(args.out / "synthetic_degradation_summary.json", {"rows": synthetic_summary})
    write_csv(args.out / "dias_per_frame_metrics.csv", dias_rows)
    write_json(args.out / "dias_per_frame_metrics.json", {"rows": dias_rows})
    write_csv(args.out / "dias_analog_summary.csv", dias_analog_rows)
    write_json(args.out / "dias_analog_summary.json", {"rows": dias_analog_rows})
    write_csv(args.out / "model_summary.csv", summary_rows)
    write_json(args.out / "model_summary.json", {"rows": summary_rows})
    write_csv(args.out / "model_ranking_rows.csv", ranks)
    write_json(args.out / "model_ranking_rows.json", {"rows": ranks, "comparison": order_compare})

    metrics: dict[str, float] = {
        **BASELINE_METRICS,
        "s2c_model_count": float(len(MODEL_PANEL)),
        "s2c_synthetic_item_count_per_model": float(len(synthetic_inputs)),
        "s2c_dias_frame_count_per_model": float(len(dias_inputs)),
        "s2c_total_prediction_count": float(len(synthetic_rows) + len(dias_rows)),
        "s2c_ranked_model_count": float(len(summary_rows)),
        "s2c_finite_metric_check": 1.0,
    }
    for row in summary_rows:
        prefix = f"s2c_{row['model_id']}"
        for key, value in row.items():
            if key == "model_id":
                continue
            metrics[f"{prefix}_{key}"] = float(value)
    if order_compare["spearman_synthetic_mean_stressor_dice_vs_dias_mean_dice"] is not None:
        metrics["s2c_spearman_synthetic_mean_vs_dias_mean_dice"] = float(
            order_compare["spearman_synthetic_mean_stressor_dice_vs_dias_mean_dice"]
        )
    metric_values = [v for v in metrics.values() if isinstance(v, (float, int))]
    if not all(np.isfinite(metric_values)):
        metrics["s2c_finite_metric_check"] = 0.0
        raise ValueError("nonfinite metric detected")
    write_json(args.out / "metrics_summary.json", metrics)

    manifest = {
        "run_id": RUN_ID,
        "parent_run_id": "run-angiostress-s2b-frozen-model-panel-smoke",
        "device": device,
        "models": model_records,
        "dias_sample": {
            "sequence_id": dias_sample["sequence_id"],
            "split": dias_sample["split"],
            "frame_count_evaluated": len(dias_inputs),
            "prompt_source": "DIAS sequence-level mask bbox; smoke-test oracle prompt, not a deployable prompt source",
            "prompt_box_xyxy": [float(x) for x in dias_box.tolist()],
        },
        "synthetic_surface": {
            "source_run_id": "run-angiostress-s0s1-renderer-smoke",
            "item_count_evaluated": len(synthetic_inputs),
            "prompt_source": "TopCoW projected GT bbox; smoke-test oracle prompt, not a deployable prompt source",
            "prompt_box_xyxy": [float(x) for x in synthetic_box.tolist()],
        },
        "outputs": {
            "synthetic_per_cell_metrics": "synthetic_per_cell_metrics.json",
            "synthetic_degradation_summary": "synthetic_degradation_summary.json",
            "dias_per_frame_metrics": "dias_per_frame_metrics.json",
            "dias_analog_summary": "dias_analog_summary.json",
            "model_summary": "model_summary.json",
            "model_ranking_rows": "model_ranking_rows.json",
            "metrics_summary": "metrics_summary.json",
        },
        "ordering_comparison": order_compare,
        "claim_boundary": (
            "Frozen-model panel smoke only. This verifies three frozen public models can be evaluated on shared "
            "synthetic and DIAS surfaces, but it does not estimate construct validity or clinical accuracy."
        ),
    }
    write_json(args.out / "manifest.json", manifest)
    write_json(
        args.out / "environment.json",
        {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
            "torch": torch.__version__,
            "device": device,
        },
    )
    write_run_notes(args.out, args, device, metrics, summary_rows, order_compare)
    return {
        "metrics": metrics,
        "model_summary_rows": summary_rows,
        "ordering_comparison": order_compare,
        "synthetic_rows": synthetic_rows,
        "dias_rows": dias_rows,
        "dias_analog_rows": dias_analog_rows,
    }


def write_run_notes(
    out_dir: Path,
    args: argparse.Namespace,
    device: str,
    metrics: dict[str, float],
    summary_rows: list[dict[str, Any]],
    order_compare: dict[str, Any],
) -> None:
    command = " ".join(sys.argv)
    run_md = f"""# RUN

## Identity

- run_id: `{RUN_ID}`
- parent_run_id: `run-angiostress-s2b-frozen-model-panel-smoke`
- command: `{command}`
- device: `{device}`

## Inputs

- Synthetic source: `experiments/main/run-angiostress-s0s1-renderer-smoke/outputs`
- DIAS source: `experiments/main/run-angiostress-s2-real-dsa-loader-smoke/outputs/real_dsa_loader_manifest.json`
- Model panel: SAM ViT-B, MedSAM ViT-B, and SAM ViT-L, all frozen.

## Method

All models are evaluated through `segment_anything` `SamPredictor` with identical label-derived bounding-box prompts. The synthetic surface uses the deterministic TopCoW projection and stressor cells; the real surface uses DIAS `s40` frames and deterministic frame-subset analogs.

## Claim Boundary

This is a frozen-model panel smoke. It creates comparable three-model ordering rows and a smoke rank diagnostic, but it does not estimate construct validity, confidence intervals, or clinical accuracy.
"""
    validation_md = f"""# VALIDATION

## Checks

- outputs_exist: true
- finite_metric_check: `{metrics["s2c_finite_metric_check"]}`
- model_count: `{metrics["s2c_model_count"]}`
- synthetic_item_count_per_model: `{metrics["s2c_synthetic_item_count_per_model"]}`
- dias_frame_count_per_model: `{metrics["s2c_dias_frame_count_per_model"]}`
- total_prediction_count: `{metrics["s2c_total_prediction_count"]}`
- ranked_model_count: `{metrics["s2c_ranked_model_count"]}`

## Model Summary Rows

{json.dumps(summary_rows, indent=2)}

## Ordering Boundary

{json.dumps(order_compare, indent=2)}

## Caveats

- DIAS `s40` has a sequence-level mask, so per-frame phase summaries remain approximate.
- Prompts are label-derived smoke-test oracle prompts, not deployable prompts.
- Three models can produce a smoke rank diagnostic, but not a stable construct-validity estimate or confidence interval.
"""
    (out_dir.parent / "RUN.md").write_text(run_md)
    (out_dir.parent / "VALIDATION.md").write_text(validation_md)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--workspace-root", type=Path, default=Path.cwd())
    parser.add_argument("--device", default="auto", choices=["auto", "cpu", "mps", "cuda"])
    parser.add_argument("--max-synthetic-items", type=int, default=0)
    parser.add_argument("--max-dias-frames", type=int, default=0)
    args = parser.parse_args()

    errors = []
    for device in choose_devices(args.device):
        try:
            result = evaluate_all(args, device)
            print(
                json.dumps(
                    {
                        "run_id": RUN_ID,
                        "device": device,
                        "model_summary_rows": result["model_summary_rows"],
                        "ordering_comparison": result["ordering_comparison"],
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
                args.out.mkdir(parents=True, exist_ok=True)
                write_json(args.out / "BLOCKER.json", {"run_id": RUN_ID, "errors": errors})
                raise
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
