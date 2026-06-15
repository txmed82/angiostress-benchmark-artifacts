"""Render Figure 1 for the AngioStress paper-facing evaluation package.

This adapts the paper-plot grouped bar template for a model-by-surface
comparison. The data are fixed measured outputs from S2c, S3b, and S3f.
"""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np


ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "figures" / "data" / "model_surface_dice.csv"
PNG_PATH = ROOT / "figures" / "figure1_model_surface_dice.png"
PDF_PATH = ROOT / "figures" / "figure1_model_surface_dice.pdf"

SURFACES = ["Synthetic stressors", "DIAS full test", "CathAction subset"]
LABELS = ["SAM ViT-B", "SAM ViT-L", "MedSAM ViT-B"]
MODEL_IDS = ["sam_vit_b", "sam_vit_l", "medsam_vit_b"]
COLORS = ["#7F8F84", "#8A9199", "#B88C8C"]
HATCHES = ["", "//", ".."]


plt.rcParams.update(
    {
        "text.usetex": False,
        "font.family": "serif",
        "font.serif": ["STIX Two Text", "DejaVu Serif", "Times New Roman"],
        "axes.unicode_minus": False,
        "hatch.color": "white",
        "hatch.linewidth": 1.2,
    }
)


def load_data() -> dict[str, list[float]]:
    values = {label: [] for label in LABELS}
    rows = []
    with DATA_PATH.open(newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    for surface in SURFACES:
        surface_rows = {row["model_id"]: row for row in rows if row["surface"] == surface}
        for model_id, label in zip(MODEL_IDS, LABELS):
            values[label].append(float(surface_rows[model_id]["mean_dice"]))
    return values


def main() -> None:
    data = load_data()
    x = np.arange(len(SURFACES))
    total_w = 0.78
    bar_w = total_w / len(LABELS)

    fig, ax = plt.subplots(figsize=(7.2, 3.25))
    fig.subplots_adjust(left=0.085, right=0.99, bottom=0.22, top=0.84)

    for i, (label, color, hatch) in enumerate(zip(LABELS, COLORS, HATCHES)):
        vals = data[label]
        offset = (i - len(LABELS) / 2 + 0.5) * bar_w
        bars = ax.bar(
            x + offset,
            vals,
            width=bar_w,
            color=color,
            hatch=hatch,
            edgecolor="white",
            linewidth=0.8,
            zorder=2,
            label=label,
        )
        for bar, value in zip(bars, vals):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                value + 0.018,
                f"{value:.3f}",
                ha="center",
                va="bottom",
                fontsize=7.8,
                color="#222222",
                zorder=3,
            )

    ax.set_xticks(x)
    ax.set_xticklabels(["Synthetic\nstressors", "DIAS\nfull test", "CathAction\nsubset"], fontsize=9.8)
    ax.set_ylabel("Mean Dice", fontsize=10.6)
    ax.set_ylim(0, 1.05)
    ax.set_xlim(-0.55, len(SURFACES) - 0.45)
    ax.yaxis.grid(True, color="#D8D1C7", alpha=0.55, linewidth=0.65, linestyle="--", zorder=0)
    ax.xaxis.grid(False)
    ax.set_axisbelow(True)

    for side, spine in ax.spines.items():
        if side in ("top", "right"):
            spine.set_visible(False)
        else:
            spine.set_linewidth(0.9)
            spine.set_color("#333333")

    ax.tick_params(length=0, labelsize=9.5)
    handles = [
        mpatches.Patch(facecolor=color, hatch=hatch, edgecolor="white", linewidth=0.8, label=label)
        for label, color, hatch in zip(LABELS, COLORS, HATCHES)
    ]
    ax.legend(
        handles=handles,
        fontsize=8.7,
        loc="upper center",
        bbox_to_anchor=(0.5, 1.13),
        ncol=3,
        frameon=False,
        labelspacing=0.25,
        handlelength=1.7,
        handletextpad=0.45,
        columnspacing=1.0,
    )

    PNG_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(PNG_PATH, dpi=300, facecolor="white", bbox_inches="tight", pad_inches=0.03)
    fig.savefig(PDF_PATH, facecolor="white", bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)
    print(f"saved: {PNG_PATH}")
    print(f"saved: {PDF_PATH}")


if __name__ == "__main__":
    main()
