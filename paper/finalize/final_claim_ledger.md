# Final Claim Ledger

Created: 2026-06-15T05:10:29Z

Package type: submission_package
Submission ready: True
Analysis groups ready: 8/8

## Supported Claims

### C1: supported

AngioStress currently provides a deterministic TopCoW-derived DSA-like synthetic scaffold with pixel-level ground truth and reproducibility checks for the evaluated S0/S1 stressor cells.

Key numbers:
- `stressor_cells`: 9
- `projected_gt_area_pixels`: 8233
- `deterministic_hash_match`: 1
- `clean_gt_self_dice`: 1.0
- `clean_gt_self_cldice`: 1.0

Evidence paths:
- `.ds/worktrees/idea-idea-a229721e/experiments/main/run-angiostress-s0s1-renderer-smoke/RUN.md`
- `.ds/worktrees/idea-idea-a229721e/experiments/main/run-angiostress-s0s1-renderer-smoke/RESULT.json`
- `/Users/colin/DeepScientist/quests/010/.ds/worktrees/idea-idea-a229721e/experiments/main/run-angiostress-s0s1-renderer-smoke/RUN.md`
- `/Users/colin/DeepScientist/quests/010/.ds/worktrees/idea-idea-a229721e/experiments/main/run-angiostress-s0s1-renderer-smoke/VALIDATION.md`
- `/Users/colin/DeepScientist/quests/010/.ds/worktrees/idea-idea-a229721e/experiments/main/run-angiostress-s0s1-renderer-smoke/run_renderer_smoke.py`
- `/Users/colin/DeepScientist/quests/010/.ds/worktrees/idea-idea-a229721e/experiments/main/run-angiostress-s0s1-renderer-smoke/outputs/manifest.json`
- `/Users/colin/DeepScientist/quests/010/.ds/worktrees/idea-idea-a229721e/experiments/main/run-angiostress-s0s1-renderer-smoke/outputs/metrics_summary.json`
- `/Users/colin/DeepScientist/quests/010/.ds/worktrees/idea-idea-a229721e/experiments/main/run-angiostress-s0s1-renderer-smoke/outputs/clean_preview.png`
- `paper/evidence_ledger.json`
- `paper/paper_experiment_matrix.json`

Boundaries:
- One TopCoW-derived anatomy/source case; not a full six-stressor benchmark release.

### C2: supported

The frozen-model evaluation harness produced finite measurements for SAM ViT-B, SAM ViT-L, and MedSAM ViT-B on the synthetic AngioStress surface and on real DIAS/CathAction diagnostic surfaces without backbone training or fine-tuning.

Key numbers:
- `frozen_model_count`: 3
- `s2c_dias_frame_count_per_model`: 6
- `s2c_finite_metric_check`: 1

Evidence paths:
- `.ds/worktrees/run-run-angiostress-s2c-third-frozen-model-panel-extension/experiments/main/run-angiostress-s2c-third-frozen-model-panel-extension/RUN.md`
- `.ds/worktrees/run-run-angiostress-s2c-third-frozen-model-panel-extension/experiments/main/run-angiostress-s2c-third-frozen-model-panel-extension/RESULT.json`
- `.ds/worktrees/run-run-angiostress-s2c-third-frozen-model-panel-extension/experiments/main/run-angiostress-s2c-third-frozen-model-panel-extension/outputs/metrics_summary.json`
- `.ds/worktrees/run-run-angiostress-s2c-third-frozen-model-panel-extension/experiments/main/run-angiostress-s2c-third-frozen-model-panel-extension/outputs/model_summary.json`
- `.ds/worktrees/run-run-angiostress-s2c-third-frozen-model-panel-extension/experiments/main/run-angiostress-s2c-third-frozen-model-panel-extension/outputs/model_ranking_rows.json`
- `.ds/worktrees/run-run-angiostress-s2c-third-frozen-model-panel-extension/experiments/main/run-angiostress-s2c-third-frozen-model-panel-extension/outputs/dias_per_frame_metrics.json`
- `.ds/worktrees/run-run-angiostress-s2c-third-frozen-model-panel-extension/experiments/main/run-angiostress-s2c-third-frozen-model-panel-extension/outputs/synthetic_per_cell_metrics.json`
- `.ds/worktrees/run-run-angiostress-s2c-third-frozen-model-panel-extension/experiments/main/run-angiostress-s2c-third-frozen-model-panel-extension/RUN.md`
- `.ds/worktrees/run-run-angiostress-s2c-third-frozen-model-panel-extension/experiments/main/run-angiostress-s2c-third-frozen-model-panel-extension/VALIDATION.md`
- `paper/tables/table1_rank_summary.md`
- `paper/figures/data/model_surface_dice.csv`

Boundaries:
- Promptable segmentation panel only; no new model training, no clinical outcome evaluation.

### C3: supported_negative_mixed

On the full DIAS test-split diagnostic, the real-model ordering is discordant with the synthetic ordering, so DIAS does not support a positive synthetic-to-real construct-validity claim in this package.

Key numbers:
- `dias_sequences`: 20
- `frames_per_model`: 115
- `prediction_count`: 345
- `dias_order`: MedSAM ViT-B > SAM ViT-L > SAM ViT-B
- `synthetic_order_reference`: SAM ViT-L > SAM ViT-B > MedSAM ViT-B
- `spearman_vs_synthetic`: -0.5
- `kendall_vs_synthetic`: -0.3333333333333333
- `bootstrap_spearman_mean`: -0.425
- `bootstrap_spearman_ci`: [-0.675, -0.125]

Evidence paths:
- `artifacts/reports/report-fe9dabda.json`
- `/Users/colin/DeepScientist/quests/010/artifacts/reports/report-fe9dabda.json`
- `experiments/analysis/s3b-dias-full-test-split-ranking/RUN.md`
- `experiments/analysis/s3b-dias-full-test-split-ranking/VALIDATION.md`
- `experiments/analysis/s3b-dias-full-test-split-ranking/outputs/model_summary.json`
- `experiments/analysis/s3b-dias-full-test-split-ranking/outputs/ranking_diagnostics.json`
- `experiments/analysis/s3b-dias-full-test-split-ranking/outputs/per_sequence_summary.json`
- `paper/figures/data/model_surface_dice.csv`
- `paper/tables/table1_rank_summary.md`

Boundaries:
- Rank diagnostic over three models; interval is a diagnostic bootstrap, not a final benchmark-wide confidence interval.

### C4: supported_partial

On the CathAction fixed human-segmentation subset, rank transfer is partial: MedSAM ViT-B remains weakest, but SAM ViT-B and SAM ViT-L swap order relative to the synthetic surface.

Key numbers:
- `nonempty_universe`: 5225
- `excluded_empty_masks`: 58
- `pairs_per_model`: 128
- `prediction_count`: 384
- `cathaction_order`: SAM ViT-B > SAM ViT-L > MedSAM ViT-B
- `synthetic_order_reference`: SAM ViT-L > SAM ViT-B > MedSAM ViT-B
- `spearman_vs_synthetic`: 0.5
- `bootstrap_spearman_mean`: 0.5285
- `bootstrap_spearman_interval`: [0.5, 1.0]
- `observed_order_match_rate`: 0.943
- `synthetic_order_match_rate`: 0.057

Evidence paths:
- `artifacts/reports/report-97c8091c.json`
- `experiments/analysis/s3f-cathaction-human-segmentation-subset-ranking/RUN.md`
- `experiments/analysis/s3f-cathaction-human-segmentation-subset-ranking/VALIDATION.md`
- `experiments/analysis/s3f-cathaction-human-segmentation-subset-ranking/outputs/metrics_summary.json`
- `experiments/analysis/s3f-cathaction-human-segmentation-subset-ranking/outputs/model_summary.json`
- `experiments/analysis/s3f-cathaction-human-segmentation-subset-ranking/outputs/model_ranking_rows.json`
- `experiments/analysis/s3f-cathaction-human-segmentation-subset-ranking/outputs/stability_summary.json`
- `experiments/analysis/s3f-cathaction-human-segmentation-subset-ranking/outputs/cleanup_status.json`
- `paper/figures/data/model_surface_dice.csv`
- `paper/tables/table1_rank_summary.md`

Boundaries:
- Fixed human-segmentation subset; not a full CathAction population estimate.

### C5: supported_boundary

The manuscript explicitly limits claims to measurement and construct-validity diagnostics, excluding clinical-accuracy claims, sim-to-real transfer claims, a final leaderboard, a complete six-stressor release, and a final construct-validity estimate.

Key numbers:
- `language_firewall_ok`: True
- `clinical_accuracy_term_hits`: 0
- `checkpoint_term_hits`: 0
- `worktree_term_hits`: 0
- `route_term_hits`: 0

Evidence paths:
- `paper/draft.md`
- `paper/manuscript_language_validation.json`
- `paper/review/submission_checklist.json`

Boundaries:
- Boundary phrases are intentionally present where the manuscript states what it does not claim.

## Unsupported Or Deferred Claims
- `unsupported_excluded`: Clinical accuracy or clinical outcome performance
- `unsupported_excluded`: Sim-to-real transfer as a positive method claim
- `deferred`: A final leaderboard for frozen endovascular perception models
- `deferred`: A complete six-stressor AngioStress v0.1 benchmark release
- `deferred`: A final high-confidence construct-validity estimate across all planned stressors and datasets
- `unsupported_excluded`: Any trained, fine-tuned, or improved backbone result

## Integrity Caveats
- Formal validators are green, but final readiness is judged from evidence provenance, claim scope, citation coverage, and package inventory as well as validator status.
- The paper files and coverage validator report 8/8 analysis groups; an earlier artifact-contract read collapsed the embedded matrix to 6 rows, so future agents should trust paper/paper_experiment_matrix.json plus paper/manuscript_coverage.json for this package state unless the generator is repaired.
- Tectonic compilation is successful with five nonfatal overfull hbox warnings.
