# Table 1: Current Rank-Transfer Evidence

| Surface | Evaluation scope | Mean Dice order | Rank diagnostic vs. synthetic order | Boundary |
| --- | --- | --- | --- | --- |
| Synthetic stressors | S2c deterministic TopCoW-derived stressor cells | SAM ViT-L (0.962), SAM ViT-B (0.893), MedSAM ViT-B (0.268) | reference order | Synthetic benchmark surface only |
| DIAS full test | S3b, 20 labeled test sequences, 115 frames per model, 345 predictions | MedSAM ViT-B (0.295), SAM ViT-L (0.263), SAM ViT-B (0.240) | Spearman -0.5; Kendall -0.333; sequence-bootstrap Spearman mean -0.425, 95% CI [-0.675, -0.125] | Discordant real-angiography ordering under the fixed prompt/metric protocol |
| CathAction subset | S3f, 128 nonempty human-segmentation pairs per model, 384 predictions | SAM ViT-B (0.365), SAM ViT-L (0.346), MedSAM ViT-B (0.100) | Spearman 0.5; fixed-subset bootstrap Spearman mean 0.5285, percentile interval [0.5, 1.0] | Partial agreement: MedSAM remains last, but SAM ViT-B and SAM ViT-L swap relative to synthetic |

Interpretation: the current evidence supports a reproducible benchmark and an honest mixed construct-validity estimate. It does not support a final clinical-accuracy claim, a sim-to-real transfer claim, or a stable real-world leaderboard.
