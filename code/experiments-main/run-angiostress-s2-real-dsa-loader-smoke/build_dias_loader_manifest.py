#!/usr/bin/env python3
"""Build a minimal DIAS real-DSA loader manifest for AngioStress."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from collections import defaultdict
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


IMAGE_RE = re.compile(r"^DIAS/(?P<split>[^/]+)/images/image_s(?P<seq>\d+)_i(?P<frame>\d+)\.png$")
LABEL_RE = re.compile(r"^DIAS/(?P<split>[^/]+)/labels/label_s(?P<seq>\d+)\.png$")


def hash_bytes(data: bytes) -> dict[str, str]:
    return {
        "md5": hashlib.md5(data).hexdigest(),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def hash_file(path: Path) -> dict[str, str | int]:
    md5 = hashlib.md5()
    sha = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8 * 1024 * 1024), b""):
            md5.update(chunk)
            sha.update(chunk)
    return {"md5": md5.hexdigest(), "sha256": sha.hexdigest(), "size_bytes": path.stat().st_size}


def image_stats(img: Image.Image) -> dict[str, object]:
    arr = np.asarray(img)
    if arr.ndim == 3:
        gray = np.asarray(img.convert("L"))
    else:
        gray = arr
    stats: dict[str, object] = {
        "mode": img.mode,
        "size_xy": list(img.size),
        "array_shape": list(arr.shape),
        "dtype": str(arr.dtype),
        "min": int(gray.min()),
        "max": int(gray.max()),
        "mean": float(gray.mean()),
        "std": float(gray.std()),
        "nonzero_pixels": int(np.count_nonzero(gray)),
    }
    nz = np.argwhere(gray > 0)
    if nz.size:
        y0, x0 = nz.min(axis=0)
        y1, x1 = nz.max(axis=0)
        stats["nonzero_bbox_xyxy"] = [int(x0), int(y0), int(x1), int(y1)]
    else:
        stats["nonzero_bbox_xyxy"] = None
    return stats


def safe_extract_member(zf: zipfile.ZipFile, member: str, dest: Path) -> dict[str, object]:
    data = zf.read(member)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    img = Image.open(dest)
    img.load()
    return {
        "archive_member": member,
        "extracted_path": str(dest),
        "source_hashes": hash_bytes(data),
        "stats": image_stats(img),
    }


def build_inventory(zf: zipfile.ZipFile) -> tuple[dict[tuple[str, str], dict[str, object]], list[str]]:
    seqs: dict[tuple[str, str], dict[str, object]] = defaultdict(lambda: {"images": [], "label": None})
    unmatched: list[str] = []
    for info in zf.infolist():
        name = info.filename
        if name.endswith("/"):
            continue
        image_match = IMAGE_RE.match(name)
        if image_match:
            key = (image_match.group("split"), f"s{image_match.group('seq')}")
            seqs[key]["images"].append(
                {
                    "frame_index": int(image_match.group("frame")),
                    "archive_member": name,
                    "size_bytes": info.file_size,
                }
            )
            continue
        label_match = LABEL_RE.match(name)
        if label_match:
            key = (label_match.group("split"), f"s{label_match.group('seq')}")
            seqs[key]["label"] = {"archive_member": name, "size_bytes": info.file_size}
            continue
        unmatched.append(name)
    for item in seqs.values():
        item["images"] = sorted(item["images"], key=lambda r: r["frame_index"])
    return seqs, unmatched


def make_preview(frame_paths: list[Path], label_path: Path, preview_path: Path) -> None:
    selected = [0, len(frame_paths) // 2, len(frame_paths) - 1]
    thumbs = []
    label = Image.open(label_path).convert("L")
    label_mask = np.asarray(label) > 0
    for idx in selected:
        img = Image.open(frame_paths[idx]).convert("RGB")
        overlay = img.copy()
        red = Image.new("RGB", img.size, (255, 0, 0))
        mask = Image.fromarray(label_mask.astype(np.uint8) * 90).convert("L")
        overlay = Image.composite(red, overlay, mask)
        overlay.thumbnail((300, 300))
        canvas = Image.new("RGB", (300, 330), "white")
        canvas.paste(overlay, ((300 - overlay.width) // 2, 0))
        draw = ImageDraw.Draw(canvas)
        draw.text((10, 306), f"frame {idx}", fill=(0, 0, 0))
        thumbs.append(canvas)
    preview = Image.new("RGB", (300 * len(thumbs), 330), "white")
    for i, thumb in enumerate(thumbs):
        preview.paste(thumb, (300 * i, 0))
    preview_path.parent.mkdir(parents=True, exist_ok=True)
    preview.save(preview_path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--zip", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--split", default="test")
    parser.add_argument("--sequence", default="s40")
    parser.add_argument("--dias-repo-head", required=True)
    parser.add_argument("--cathaction-repo-head", required=True)
    args = parser.parse_args()

    zip_path = Path(args.zip)
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    sample_dir = out_dir / "sample" / args.sequence
    frame_dir = sample_dir / "frames"
    label_dir = sample_dir / "labels"

    archive_hashes = hash_file(zip_path)
    published_md5 = "780f32df6fb2a5de5d476f385cf2e83b"
    selected_key = (args.split, args.sequence)

    with zipfile.ZipFile(zip_path) as zf:
        inventory, unmatched = build_inventory(zf)
        selected = inventory.get(selected_key)
        if not selected:
            raise SystemExit(f"Missing selected sequence {selected_key}")
        images = selected["images"]
        label = selected["label"]
        if not images or not label:
            raise SystemExit(f"Selected sequence {selected_key} lacks images or sequence label")

        frame_records = []
        for row in images:
            member = row["archive_member"]
            frame_path = frame_dir / Path(member).name
            record = safe_extract_member(zf, member, frame_path)
            record["frame_index"] = row["frame_index"]
            frame_records.append(record)

        label_path = label_dir / Path(label["archive_member"]).name
        label_record = safe_extract_member(zf, label["archive_member"], label_path)

    preview_path = out_dir / "dias_s40_preview.png"
    make_preview([Path(r["extracted_path"]) for r in frame_records], label_path, preview_path)

    split_counts = defaultdict(int)
    paired_counts = defaultdict(int)
    sequence_rows = []
    for (split, seq), item in sorted(inventory.items(), key=lambda kv: (kv[0][0], kv[0][1])):
        image_count = len(item["images"])
        has_label = item["label"] is not None
        split_counts[split] += 1
        if image_count and has_label:
            paired_counts[split] += 1
        sequence_rows.append(
            {
                "split": split,
                "sequence_id": seq,
                "image_count": image_count,
                "has_sequence_label": has_label,
                "frame_indices": [r["frame_index"] for r in item["images"]],
            }
        )

    manifest = {
        "schema_version": 1,
        "run_id": "run-angiostress-s2-real-dsa-loader-smoke",
        "created_by": "build_dias_loader_manifest.py",
        "claim_boundary": "DIAS real-data loader feasibility and stressor-analog schema only; no construct-validity estimate or clinical claim.",
        "sources": {
            "dias_archive": {
                "path": str(zip_path),
                "zenodo_record_api": "https://zenodo.org/api/records/11396520",
                "zenodo_record_id_resolved": 11637181,
                "published_file": "DIAS.zip",
                "published_md5": published_md5,
                **archive_hashes,
                "md5_matches_published": archive_hashes["md5"] == published_md5,
            },
            "dias_repo": {
                "url": "https://github.com/lseventeen/DIAS",
                "head_commit": args.dias_repo_head,
            },
            "cathaction_repo": {
                "url": "https://github.com/airvlab/cathaction",
                "head_commit": args.cathaction_repo_head,
                "local_data_status": "source_audited_not_loaded",
                "reason": "Project site and Hugging Face listing indicate a download/license flow; no CathAction dataset archive was locally loaded in this bounded DIAS-first smoke.",
            },
        },
        "dataset_inventory": {
            "sequence_count": len(sequence_rows),
            "split_counts": dict(sorted(split_counts.items())),
            "paired_sequence_counts": dict(sorted(paired_counts.items())),
            "unmatched_archive_member_count": len(unmatched),
            "sequence_rows_preview": sequence_rows[:20],
        },
        "selected_sample": {
            "dataset": "DIAS",
            "split": args.split,
            "sequence_id": args.sequence,
            "frame_count": len(frame_records),
            "frame_records": frame_records,
            "label_record": label_record,
            "preview_path": str(preview_path),
        },
        "stressor_analog_mapping": {
            "frame_thinning": {
                "status": "available_for_dias_sequence",
                "definition": "Use deterministic frame-index subsampling over a real DIAS sequence.",
                "candidate_severity_parameters": [
                    {"severity": 0, "keep_every_nth_frame": 1},
                    {"severity": 1, "keep_every_nth_frame": 2},
                    {"severity": 2, "keep_every_nth_frame": 3},
                ],
            },
            "contrast_phase": {
                "status": "available_for_dias_sequence",
                "definition": "Use deterministic early/middle/late frame windows and intensity summaries as real contrast-phase analogs.",
                "candidate_severity_parameters": [
                    {"severity": 0, "window": "all_frames"},
                    {"severity": 1, "window": "early_or_late_half"},
                    {"severity": 2, "window": "single_extreme_phase_frame"},
                ],
            },
            "device_overlay": {
                "status": "not_available_from_dias_loader_alone",
                "definition": "Requires CathAction catheter/guidewire masks or a separately justified real-device annotation source.",
                "current_boundary": "CathAction code/site are source-audited, but the dataset was not locally loaded in this node.",
            },
        },
    }

    manifest_path = out_dir / "real_dsa_loader_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True))
    print(
        json.dumps(
            {
                "manifest_path": str(manifest_path),
                "preview_path": str(preview_path),
                "sequence_count": manifest["dataset_inventory"]["sequence_count"],
                "split_counts": manifest["dataset_inventory"]["split_counts"],
                "selected_frame_count": len(frame_records),
                "label_nonzero_pixels": label_record["stats"]["nonzero_pixels"],
                "md5_matches_published": manifest["sources"]["dias_archive"]["md5_matches_published"],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
