# AngioStress S1 frozen-model harness smoke with SAM ViT-B

- Run id: `run-angiostress-s1-frozen-model-smoke`
- Branch: `run/run-angiostress-s1-frozen-model-smoke`
- Parent branch: `run/run-angiostress-s0s1-renderer-smoke`
- Worktree: `/Users/colin/DeepScientist/quests/010/.ds/worktrees/run-angiostress-s1-frozen-model-smoke`
- Idea: `idea-a229721e`
- Baseline: `angiostress-s0-topcow-resencm`
- Baseline variant: `one_case_topcow_resencm_1000ep`
- Dataset scope: `generated s0/s1 topcow-derived angiostress cells from parent run run-angiostress-s0s1-renderer-smoke: clean plus 9 stressed cells across frame thinning, contrast phase, and device overlay. no dias/cathaction real-data inference in this run.`
- Verdict: `supported_for_frozen_model_harness_smoke_not_construct_validity`
- Status: `completed`

## Hypothesis

A frozen off-the-shelf promptable 2D model can be run over the generated clean/stressed AngioStress cells without training, producing per-cell degradation metrics against projected GT while preserving stressor family/severity metadata.

## Setup

Created a child run branch/worktree from the renderer-smoke result. The active environment lacked torch/torchvision/segment-anything/MedSAM/nnU-Net packages, so an isolated quest-local virtualenv was created. Installed torch 2.8.0, torchvision 0.23.0, segment-anything 1.0, and scikit-image for metrics. Downloaded the public SAM ViT-B checkpoint, SHA256 ec2df62732614e57411cdcf32a23ffdf28910380d03139ee0f4fcbe91eb8c912. SAM was frozen and prompted with the projected-GT bounding box for this smoke pass.

## Execution

Compile-checked the evaluator, ran SAM ViT-B on MPS over clean plus 9 stressed cells, wrote per-cell prediction masks and metrics, validated required output files and finite numeric metrics, and visually inspected clean and device-overlay severity 2 prediction PNGs. The first evaluator attempt failed before inference due missing scikit-image in the isolated venv; after installing that metric dependency, the rerun completed successfully.

## Results

SAM ViT-B produced 10 prediction rows and 10 mask PNG/NPY outputs. Clean Dice was 0.9810482128526452 and clean clDice was 0.9990412272291467. Across 9 stressed cells, mean Dice was 0.892633475863582 and mean clDice was 0.920166815700077. Mean Dice delta vs clean was -0.08841473698906317. Device overlay was the strongest observed degradation family: mean Dice 0.7218091541803723, mean clDice 0.76477019540269. The strongest single cell was device_overlay_severity_2 with Dice 0.6241094597782496, clDice 0.6424506218998289, and component-count ratio 66.0.

## Conclusion

The frozen-model harness smoke is supported: one off-the-shelf frozen promptable model runs over AngioStress generated cells and produces per-cell degradation metrics. This is not a final medical comparator or construct-validity estimate; it establishes the next bridge toward DIAS/CathAction real-data analogs.

## Metrics Summary

- `topcow_resencm_one_case_mean_dice` = 0.6985
- `topcow_resencm_one_case_mean_cldice` = 0.6285
- `topcow_resencm_one_case_graph_ready_rate` = 1
- `topcow_gt_sanity_mean_dice` = 1
- `topcow_gt_sanity_mean_cldice` = 1
- `topcow_gt_sanity_graph_ready_rate` = 1
- `topcow_resencm_checkpoint_train_mean_dice` = 0.7261
- `sam_vit_b_prediction_row_count` = 10
- `sam_vit_b_stressor_cell_count` = 9
- `sam_vit_b_clean_dice` = 0.981
- `sam_vit_b_clean_cldice` = 0.999
- `sam_vit_b_mean_stressor_dice` = 0.8926
- `sam_vit_b_mean_stressor_cldice` = 0.9202
- `sam_vit_b_mean_stressor_dice_delta_vs_clean` = -0.0884
- `sam_vit_b_mean_stressor_cldice_delta_vs_clean` = -0.0789
- `sam_vit_b_min_stressor_dice` = 0.5603
- `sam_vit_b_min_stressor_cldice` = 0.6425
- `sam_vit_b_frame_thinning_mean_dice` = 0.9798
- `sam_vit_b_contrast_phase_mean_dice` = 0.9763
- `sam_vit_b_device_overlay_mean_dice` = 0.7218
- `sam_vit_b_device_overlay_severity2_dice` = 0.6241
- `sam_vit_b_device_overlay_severity2_cldice` = 0.6425
- `sam_vit_b_device_overlay_severity2_component_count_ratio` = 66
- `sam_vit_b_finite_metric_check` = 1

## Baseline Comparison

- `topcow_resencm_one_case_mean_dice`: run=0.6985 baseline=0.6985 delta=0 (worse)
- `topcow_resencm_one_case_mean_cldice`: run=0.6285 baseline=0.6285 delta=0 (worse)
- `topcow_resencm_one_case_graph_ready_rate`: run=1 baseline=1 delta=0 (worse)
- `topcow_gt_sanity_mean_dice`: run=1 baseline=1 delta=0 (worse)
- `topcow_gt_sanity_mean_cldice`: run=1 baseline=1 delta=0 (worse)
- `topcow_gt_sanity_graph_ready_rate`: run=1 baseline=1 delta=0 (worse)
- `topcow_resencm_checkpoint_train_mean_dice`: run=0.7261 baseline=0.7261 delta=0 (worse)
- `sam_vit_b_clean_dice`: run=0.981 baseline=None delta=n/a (not comparable)
- `sam_vit_b_clean_cldice`: run=0.999 baseline=None delta=n/a (not comparable)
- `sam_vit_b_mean_stressor_dice`: run=0.8926 baseline=None delta=n/a (not comparable)
- `sam_vit_b_mean_stressor_cldice`: run=0.9202 baseline=None delta=n/a (not comparable)
- `sam_vit_b_mean_stressor_dice_delta_vs_clean`: run=-0.0884 baseline=None delta=n/a (not comparable)
- `sam_vit_b_device_overlay_mean_dice`: run=0.7218 baseline=None delta=n/a (not comparable)
- `sam_vit_b_device_overlay_severity2_dice`: run=0.6241 baseline=None delta=n/a (not comparable)
- `sam_vit_b_device_overlay_severity2_component_count_ratio`: run=66 baseline=None delta=n/a (not comparable)
- `sam_vit_b_prediction_row_count`: run=10 baseline=None delta=n/a (not comparable)
- `sam_vit_b_stressor_cell_count`: run=9 baseline=None delta=n/a (not comparable)
- `sam_vit_b_mean_stressor_cldice_delta_vs_clean`: run=-0.0789 baseline=None delta=n/a (not comparable)
- `sam_vit_b_min_stressor_dice`: run=0.5603 baseline=None delta=n/a (not comparable)
- `sam_vit_b_min_stressor_cldice`: run=0.6425 baseline=None delta=n/a (not comparable)
- `sam_vit_b_frame_thinning_mean_dice`: run=0.9798 baseline=None delta=n/a (not comparable)
- `sam_vit_b_contrast_phase_mean_dice`: run=0.9763 baseline=None delta=n/a (not comparable)
- `sam_vit_b_device_overlay_severity2_cldice`: run=0.6425 baseline=None delta=n/a (not comparable)
- `sam_vit_b_finite_metric_check`: run=1 baseline=None delta=n/a (not comparable)

## Changed Files

- `plan.md`
- `PLAN.md`
- `CHECKLIST.md`
- `status.md`
- `experiments/main/run-angiostress-s1-frozen-model-smoke/config.json`
- `experiments/main/run-angiostress-s1-frozen-model-smoke/RUN.md`
- `experiments/main/run-angiostress-s1-frozen-model-smoke/VALIDATION.md`
- `experiments/main/run-angiostress-s1-frozen-model-smoke/DEPENDENCY_AUDIT.md`
- `experiments/main/run-angiostress-s1-frozen-model-smoke/run_sam_smoke.py`
- `experiments/main/run-angiostress-s1-frozen-model-smoke/outputs/manifest.json`
- `experiments/main/run-angiostress-s1-frozen-model-smoke/outputs/metrics_summary.json`
- `experiments/main/run-angiostress-s1-frozen-model-smoke/outputs/per_cell_metrics.json`
- `experiments/main/run-angiostress-s1-frozen-model-smoke/outputs/per_cell_metrics.csv`

## Evidence Paths

- `/Users/colin/DeepScientist/quests/010/.ds/worktrees/run-angiostress-s1-frozen-model-smoke/experiments/main/run-angiostress-s1-frozen-model-smoke/RUN.md`
- `/Users/colin/DeepScientist/quests/010/.ds/worktrees/run-angiostress-s1-frozen-model-smoke/experiments/main/run-angiostress-s1-frozen-model-smoke/VALIDATION.md`
- `/Users/colin/DeepScientist/quests/010/.ds/worktrees/run-angiostress-s1-frozen-model-smoke/experiments/main/run-angiostress-s1-frozen-model-smoke/DEPENDENCY_AUDIT.md`
- `/Users/colin/DeepScientist/quests/010/.ds/worktrees/run-angiostress-s1-frozen-model-smoke/experiments/main/run-angiostress-s1-frozen-model-smoke/run_sam_smoke.py`
- `/Users/colin/DeepScientist/quests/010/.ds/worktrees/run-angiostress-s1-frozen-model-smoke/experiments/main/run-angiostress-s1-frozen-model-smoke/outputs/manifest.json`
- `/Users/colin/DeepScientist/quests/010/.ds/worktrees/run-angiostress-s1-frozen-model-smoke/experiments/main/run-angiostress-s1-frozen-model-smoke/outputs/metrics_summary.json`
- `/Users/colin/DeepScientist/quests/010/.ds/worktrees/run-angiostress-s1-frozen-model-smoke/experiments/main/run-angiostress-s1-frozen-model-smoke/outputs/per_cell_metrics.csv`
- `/Users/colin/DeepScientist/quests/010/.ds/worktrees/run-angiostress-s1-frozen-model-smoke/experiments/main/run-angiostress-s1-frozen-model-smoke/outputs/predictions/clean_mask.png`
- `/Users/colin/DeepScientist/quests/010/.ds/worktrees/run-angiostress-s1-frozen-model-smoke/experiments/main/run-angiostress-s1-frozen-model-smoke/outputs/predictions/device_overlay_severity_2_mask.png`

## Config Paths

- `/Users/colin/DeepScientist/quests/010/.ds/worktrees/run-angiostress-s1-frozen-model-smoke/experiments/main/run-angiostress-s1-frozen-model-smoke/config.json`

## Notes

- SAM ViT-B is a generic promptable frozen model; this run is useful for harness validation but is not a final medical comparator.
- No model training or fine-tuning was performed.
- The GT-derived box prompt is acceptable for this smoke pass but must be described transparently in later benchmark protocol.
- DIAS/CathAction real-data loading and synthetic-to-real rank correlation remain downstream.

## Evaluation Summary

- Not recorded.

## Delivery Policy

- Research paper required: `True`
- Recommended next route: `revise_idea`
- Reason: Research paper mode is enabled, but the current run does not beat the baseline clearly enough. Revise the direction or strengthen the method before writing.
