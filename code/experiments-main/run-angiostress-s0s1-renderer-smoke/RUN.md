# AngioStress S0/S1 renderer-smoke benchmark artifact

- Run id: `run-angiostress-s0s1-renderer-smoke`
- Branch: `run/run-angiostress-s0s1-renderer-smoke`
- Parent branch: `idea/010-idea-a229721e`
- Worktree: `/Users/colin/DeepScientist/quests/010/.ds/worktrees/idea-idea-a229721e`
- Idea: `idea-a229721e`
- Baseline: `angiostress-s0-topcow-resencm`
- Baseline variant: `one_case_topcow_resencm_1000ep`
- Dataset scope: `one accepted topcow circle-of-willis source case: topcow_cta_isles2024_tum_sub-stroke_0002_ct. this is source/renderer smoke evidence only, not a dias/cathaction construct-validity estimate.`
- Verdict: `supported_for_renderer_feasibility_not_construct_validity`
- Status: `completed`

## Hypothesis

The accepted TopCoW source case can be converted into a deterministic clean DSA-like projection with pixel GT and labeled S0/S1 stressor cells with finite sanity metrics, enabling the next frozen-model evaluation pass.

## Setup

Added a self-contained renderer-smoke package under experiments/main/run-angiostress-s0s1-renderer-smoke in the active idea worktree. The config points to the previously verified TopCoW volume/mask paths and uses a fixed seed. The script projects the 3D mask to a 256x256 DSA-like clean image, exports a projected GT mask, and creates three stressor families with three severity levels each.

## Execution

Ran py_compile, generated the primary outputs, generated a fresh outputs_rerun_check directory from the same config, compared primary output hashes and per-cell sequence hashes, validated required files and finite metrics, and visually inspected clean/device preview PNGs. All shell execution used bash_exec-managed sessions.

## Results

The renderer-smoke pass generated 9 stressor cells across frame thinning, contrast phase, and device overlay. Required outputs were present; the projected GT area was 8,233 pixels with 2 connected components; clean GT self Dice and self clDice were both 1.0; all numeric metrics were finite; fresh rerun output hashes and per-cell hashes matched. Frozen 2D model inference was not run in this scoped pass and is recorded as deferred.

## Conclusion

The S0/S1 renderer/stressor feasibility claim is supported for this one TopCoW case. The result does not support DIAS/CathAction construct-validity claims yet; the next evidence node should add a frozen 2D model evaluation harness or real-DSA loader bridge.

## Metrics Summary

- `topcow_resencm_one_case_mean_dice` = 0.6985
- `topcow_resencm_one_case_mean_cldice` = 0.6285
- `topcow_resencm_one_case_graph_ready_rate` = 1
- `topcow_gt_sanity_mean_dice` = 1
- `topcow_gt_sanity_mean_cldice` = 1
- `topcow_gt_sanity_graph_ready_rate` = 1
- `topcow_resencm_checkpoint_train_mean_dice` = 0.7261
- `angiostress_renderer_success` = 1
- `angiostress_renderer_cell_count` = 9
- `angiostress_renderer_family_count` = 3
- `angiostress_renderer_severity_levels_per_family` = 3
- `angiostress_renderer_deterministic_hash_match` = 1
- `angiostress_renderer_projected_gt_area_pixels` = 8233
- `angiostress_renderer_projected_gt_area_fraction` = 0.1256
- `angiostress_renderer_projected_gt_components_2d` = 2
- `angiostress_renderer_clean_gt_self_dice` = 1
- `angiostress_renderer_clean_gt_self_cldice` = 1
- `angiostress_renderer_finite_metric_check` = 1
- `angiostress_renderer_frozen_model_smoke_completed` = 0

## Baseline Comparison

- `topcow_resencm_one_case_mean_dice`: run=0.6985 baseline=0.6985 delta=0 (worse)
- `topcow_resencm_one_case_mean_cldice`: run=0.6285 baseline=0.6285 delta=0 (worse)
- `topcow_resencm_one_case_graph_ready_rate`: run=1 baseline=1 delta=0 (worse)
- `topcow_gt_sanity_mean_dice`: run=1 baseline=1 delta=0 (worse)
- `topcow_gt_sanity_mean_cldice`: run=1 baseline=1 delta=0 (worse)
- `topcow_gt_sanity_graph_ready_rate`: run=1 baseline=1 delta=0 (worse)
- `topcow_resencm_checkpoint_train_mean_dice`: run=0.7261 baseline=0.7261 delta=0 (worse)
- `angiostress_renderer_success`: run=1 baseline=None delta=n/a (not comparable)
- `angiostress_renderer_cell_count`: run=9 baseline=None delta=n/a (not comparable)
- `angiostress_renderer_deterministic_hash_match`: run=1 baseline=None delta=n/a (not comparable)
- `angiostress_renderer_projected_gt_area_pixels`: run=8233 baseline=None delta=n/a (not comparable)
- `angiostress_renderer_projected_gt_components_2d`: run=2 baseline=None delta=n/a (not comparable)
- `angiostress_renderer_frozen_model_smoke_completed`: run=0 baseline=None delta=n/a (not comparable)
- `angiostress_renderer_family_count`: run=3 baseline=None delta=n/a (not comparable)
- `angiostress_renderer_severity_levels_per_family`: run=3 baseline=None delta=n/a (not comparable)
- `angiostress_renderer_projected_gt_area_fraction`: run=0.1256 baseline=None delta=n/a (not comparable)
- `angiostress_renderer_clean_gt_self_dice`: run=1 baseline=None delta=n/a (not comparable)
- `angiostress_renderer_clean_gt_self_cldice`: run=1 baseline=None delta=n/a (not comparable)
- `angiostress_renderer_finite_metric_check`: run=1 baseline=None delta=n/a (not comparable)

## Changed Files

- `CHECKLIST.md`
- `status.md`
- `experiments/main/run-angiostress-s0s1-renderer-smoke/config.json`
- `experiments/main/run-angiostress-s0s1-renderer-smoke/RUN.md`
- `experiments/main/run-angiostress-s0s1-renderer-smoke/VALIDATION.md`
- `experiments/main/run-angiostress-s0s1-renderer-smoke/run_renderer_smoke.py`
- `experiments/main/run-angiostress-s0s1-renderer-smoke/outputs/manifest.json`
- `experiments/main/run-angiostress-s0s1-renderer-smoke/outputs/metrics_summary.json`
- `experiments/main/run-angiostress-s0s1-renderer-smoke/outputs/manifest.jsonl`

## Evidence Paths

- `/Users/colin/DeepScientist/quests/010/.ds/worktrees/idea-idea-a229721e/experiments/main/run-angiostress-s0s1-renderer-smoke/RUN.md`
- `/Users/colin/DeepScientist/quests/010/.ds/worktrees/idea-idea-a229721e/experiments/main/run-angiostress-s0s1-renderer-smoke/VALIDATION.md`
- `/Users/colin/DeepScientist/quests/010/.ds/worktrees/idea-idea-a229721e/experiments/main/run-angiostress-s0s1-renderer-smoke/run_renderer_smoke.py`
- `/Users/colin/DeepScientist/quests/010/.ds/worktrees/idea-idea-a229721e/experiments/main/run-angiostress-s0s1-renderer-smoke/outputs/manifest.json`
- `/Users/colin/DeepScientist/quests/010/.ds/worktrees/idea-idea-a229721e/experiments/main/run-angiostress-s0s1-renderer-smoke/outputs/metrics_summary.json`
- `/Users/colin/DeepScientist/quests/010/.ds/worktrees/idea-idea-a229721e/experiments/main/run-angiostress-s0s1-renderer-smoke/outputs/clean_preview.png`
- `/Users/colin/DeepScientist/quests/010/.ds/worktrees/idea-idea-a229721e/experiments/main/run-angiostress-s0s1-renderer-smoke/outputs/cells/device_overlay_severity_2.png`
- `/Users/colin/DeepScientist/quests/010/.ds/worktrees/idea-idea-a229721e/experiments/main/run-angiostress-s0s1-renderer-smoke/outputs_rerun_check/manifest.json`

## Config Paths

- `/Users/colin/DeepScientist/quests/010/.ds/worktrees/idea-idea-a229721e/experiments/main/run-angiostress-s0s1-renderer-smoke/config.json`

## Notes

- No model training or fine-tuning was performed.
- No DIAS/CathAction construct-validity or clinical-accuracy claim is made from this run.
- The accepted TopCoW ResEncM baseline remains a source/sanity comparator; the next comparison-heavy step needs a frozen 2D DSA model harness or real-DSA loader bridge.

## Evaluation Summary

- Not recorded.

## Delivery Policy

- Research paper required: `True`
- Recommended next route: `revise_idea`
- Reason: Research paper mode is enabled, but the current run does not beat the baseline clearly enough. Revise the direction or strengthen the method before writing.
