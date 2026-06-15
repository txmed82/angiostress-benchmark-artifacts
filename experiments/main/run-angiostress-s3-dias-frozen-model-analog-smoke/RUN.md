# DIAS Frozen SAM Real-Analog Smoke

- Run id: `run-angiostress-s3-dias-frozen-model-analog-smoke`
- Branch: `run/run-angiostress-s3-dias-frozen-model-analog-smoke`
- Parent branch: `run/run-angiostress-s2-real-dsa-loader-smoke`
- Worktree: `.ds/worktrees/run-angiostress-s3-dias-frozen-model-analog-smoke`
- Idea: `idea-a229721e`
- Baseline: `angiostress-s0-topcow-resencm`
- Baseline variant: `one_case_topcow_resencm_1000ep`
- Dataset scope: `one dias test sequence, s40, with 6 extracted 800x800 frames and one sequence-level vessel mask. analog families covered in this run are frame_thinning and contrast_phase; device_overlay remains deferred until cathaction or another real device-mask source is locally loaded.`
- Verdict: `supported_for_real_data_harness_smoke_not_construct_validity`
- Status: `completed`

## Hypothesis

A verified DIAS test sequence can support frozen-model real-side metric extraction for frame-thinning and contrast-phase analog families using the existing AngioStress harness.

## Setup

DIAS test sequence s40 from the verified DIAS Zenodo archive; 6 frames, one sequence-level mask, frozen SAM ViT-B checkpoint ec2df62732614e57411cdcf32a23ffdf28910380d03139ee0f4fcbe91eb8c912, label-derived bounding-box prompt, no training or fine-tuning.

## Execution

Ran tmp/angiostress-s1-venv/bin/python experiments/main/run-angiostress-s3-dias-frozen-model-analog-smoke/run_dias_sam_analog_smoke.py --manifest experiments/main/run-angiostress-s2-real-dsa-loader-smoke/outputs/real_dsa_loader_manifest.json --checkpoint tmp/angiostress-s1-weights/sam_vit_b_01ec64.pth --out experiments/main/run-angiostress-s3-dias-frozen-model-analog-smoke/outputs --device auto via bash_exec id bash-cac16b34; device resolved to MPS. Follow-up validation used bash-b01dbabe and bash-ab32173b.

## Results

The run produced finite per-frame and per-analog metrics, prediction masks, overlays, and validation records. SAM predicted nonempty masks for all 6 frames, but performance was weak under the label-derived bbox prompt: all-frame mean Dice 0.21131857528530187 and mean clDice 0.2344899136404658. Frame-thinning severity 2 had Dice delta -0.0005932835787929025 versus severity 0; contrast-phase severity 2 had Dice delta 0.0056035950660932865 versus severity 0. These are real-side harness feasibility results, not construct-validity estimates.

## Conclusion

Supported as a real-data harness smoke: AngioStress can now run a frozen off-the-shelf model on verified DIAS frames and emit finite analog-family degradation summaries. The result also shows that generic SAM with a label-derived bbox oversegments this DIAS sample, so this is a useful failure surface but not yet a model-ordering or synthetic-to-real correlation result.

## Metrics Summary

- `dias_sam_all_frame_mean_cldice` = 0.2345
- `dias_sam_all_frame_mean_dice` = 0.2113
- `dias_sam_contrast_phase_severity0_cldice_delta_vs_severity0` = 0
- `dias_sam_contrast_phase_severity0_dice_delta_vs_severity0` = 0
- `dias_sam_contrast_phase_severity0_mean_cldice` = 0.2345
- `dias_sam_contrast_phase_severity0_mean_dice` = 0.2113
- `dias_sam_contrast_phase_severity1_cldice_delta_vs_severity0` = -0.004
- `dias_sam_contrast_phase_severity1_dice_delta_vs_severity0` = 0.0011
- `dias_sam_contrast_phase_severity1_mean_cldice` = 0.2305
- `dias_sam_contrast_phase_severity1_mean_dice` = 0.2124
- `dias_sam_contrast_phase_severity2_cldice_delta_vs_severity0` = -0.028
- `dias_sam_contrast_phase_severity2_dice_delta_vs_severity0` = 0.0056
- `dias_sam_contrast_phase_severity2_mean_cldice` = 0.2065
- `dias_sam_contrast_phase_severity2_mean_dice` = 0.2169
- `dias_sam_finite_metric_check` = 1
- `dias_sam_frame_count` = 6
- `dias_sam_frame_thinning_severity0_cldice_delta_vs_severity0` = 0
- `dias_sam_frame_thinning_severity0_dice_delta_vs_severity0` = 0
- `dias_sam_frame_thinning_severity0_mean_cldice` = 0.2345
- `dias_sam_frame_thinning_severity0_mean_dice` = 0.2113
- `dias_sam_frame_thinning_severity1_cldice_delta_vs_severity0` = -0.0007
- `dias_sam_frame_thinning_severity1_dice_delta_vs_severity0` = -0.0007
- `dias_sam_frame_thinning_severity1_mean_cldice` = 0.2338
- `dias_sam_frame_thinning_severity1_mean_dice` = 0.2107
- `dias_sam_frame_thinning_severity2_cldice_delta_vs_severity0` = 0.0211
- `dias_sam_frame_thinning_severity2_dice_delta_vs_severity0` = -0.0006
- `dias_sam_frame_thinning_severity2_mean_cldice` = 0.2556
- `dias_sam_frame_thinning_severity2_mean_dice` = 0.2107
- `dias_sam_label_nonzero_pixels` = 71224
- `dias_sam_min_frame_cldice` = 0.2065
- `dias_sam_min_frame_dice` = 0.2057
- `dias_sam_prediction_nonempty_rate` = 1
- `dias_sam_prompt_bbox_area_pixels` = 610736
- `topcow_gt_sanity_graph_ready_rate` = 1
- `topcow_gt_sanity_mean_cldice` = 1
- `topcow_gt_sanity_mean_dice` = 1
- `topcow_resencm_one_case_graph_ready_rate` = 1
- `topcow_resencm_one_case_mean_cldice` = 0.6285
- `topcow_resencm_one_case_mean_dice` = 0.6985

## Baseline Comparison

- `topcow_resencm_one_case_mean_dice`: run=0.6985 baseline=0.6985 delta=0 (worse)
- `topcow_resencm_one_case_mean_cldice`: run=0.6285 baseline=0.6285 delta=0 (worse)
- `topcow_resencm_one_case_graph_ready_rate`: run=1 baseline=1 delta=0 (worse)
- `topcow_gt_sanity_mean_dice`: run=1 baseline=1 delta=0 (worse)
- `topcow_gt_sanity_mean_cldice`: run=1 baseline=1 delta=0 (worse)
- `topcow_gt_sanity_graph_ready_rate`: run=1 baseline=1 delta=0 (worse)
- `topcow_resencm_checkpoint_train_mean_dice`: run=None baseline=0.7261 delta=n/a (not comparable)
- `dias_sam_all_frame_mean_cldice`: run=0.2345 baseline=None delta=n/a (not comparable)
- `dias_sam_all_frame_mean_dice`: run=0.2113 baseline=None delta=n/a (not comparable)
- `dias_sam_contrast_phase_severity0_cldice_delta_vs_severity0`: run=0 baseline=None delta=n/a (not comparable)
- `dias_sam_contrast_phase_severity0_dice_delta_vs_severity0`: run=0 baseline=None delta=n/a (not comparable)
- `dias_sam_contrast_phase_severity0_mean_cldice`: run=0.2345 baseline=None delta=n/a (not comparable)
- `dias_sam_contrast_phase_severity0_mean_dice`: run=0.2113 baseline=None delta=n/a (not comparable)
- `dias_sam_contrast_phase_severity1_cldice_delta_vs_severity0`: run=-0.004 baseline=None delta=n/a (not comparable)
- `dias_sam_contrast_phase_severity1_dice_delta_vs_severity0`: run=0.0011 baseline=None delta=n/a (not comparable)
- `dias_sam_contrast_phase_severity1_mean_cldice`: run=0.2305 baseline=None delta=n/a (not comparable)
- `dias_sam_contrast_phase_severity1_mean_dice`: run=0.2124 baseline=None delta=n/a (not comparable)
- `dias_sam_contrast_phase_severity2_cldice_delta_vs_severity0`: run=-0.028 baseline=None delta=n/a (not comparable)
- `dias_sam_contrast_phase_severity2_dice_delta_vs_severity0`: run=0.0056 baseline=None delta=n/a (not comparable)
- `dias_sam_contrast_phase_severity2_mean_cldice`: run=0.2065 baseline=None delta=n/a (not comparable)
- `dias_sam_contrast_phase_severity2_mean_dice`: run=0.2169 baseline=None delta=n/a (not comparable)
- `dias_sam_finite_metric_check`: run=1 baseline=None delta=n/a (not comparable)
- `dias_sam_frame_count`: run=6 baseline=None delta=n/a (not comparable)
- `dias_sam_frame_thinning_severity0_cldice_delta_vs_severity0`: run=0 baseline=None delta=n/a (not comparable)
- `dias_sam_frame_thinning_severity0_dice_delta_vs_severity0`: run=0 baseline=None delta=n/a (not comparable)
- `dias_sam_frame_thinning_severity0_mean_cldice`: run=0.2345 baseline=None delta=n/a (not comparable)
- `dias_sam_frame_thinning_severity0_mean_dice`: run=0.2113 baseline=None delta=n/a (not comparable)
- `dias_sam_frame_thinning_severity1_cldice_delta_vs_severity0`: run=-0.0007 baseline=None delta=n/a (not comparable)
- `dias_sam_frame_thinning_severity1_dice_delta_vs_severity0`: run=-0.0007 baseline=None delta=n/a (not comparable)
- `dias_sam_frame_thinning_severity1_mean_cldice`: run=0.2338 baseline=None delta=n/a (not comparable)
- `dias_sam_frame_thinning_severity1_mean_dice`: run=0.2107 baseline=None delta=n/a (not comparable)
- `dias_sam_frame_thinning_severity2_cldice_delta_vs_severity0`: run=0.0211 baseline=None delta=n/a (not comparable)
- `dias_sam_frame_thinning_severity2_dice_delta_vs_severity0`: run=-0.0006 baseline=None delta=n/a (not comparable)
- `dias_sam_frame_thinning_severity2_mean_cldice`: run=0.2556 baseline=None delta=n/a (not comparable)
- `dias_sam_frame_thinning_severity2_mean_dice`: run=0.2107 baseline=None delta=n/a (not comparable)
- `dias_sam_label_nonzero_pixels`: run=71224 baseline=None delta=n/a (not comparable)
- `dias_sam_min_frame_cldice`: run=0.2065 baseline=None delta=n/a (not comparable)
- `dias_sam_min_frame_dice`: run=0.2057 baseline=None delta=n/a (not comparable)
- `dias_sam_prediction_nonempty_rate`: run=1 baseline=None delta=n/a (not comparable)
- `dias_sam_prompt_bbox_area_pixels`: run=610736 baseline=None delta=n/a (not comparable)

## Changed Files

- `experiments/main/run-angiostress-s3-dias-frozen-model-analog-smoke/run_dias_sam_analog_smoke.py`
- `experiments/main/run-angiostress-s3-dias-frozen-model-analog-smoke/RUN.md`
- `experiments/main/run-angiostress-s3-dias-frozen-model-analog-smoke/VALIDATION.md`
- `experiments/main/run-angiostress-s3-dias-frozen-model-analog-smoke/outputs/metrics_summary.json`
- `experiments/main/run-angiostress-s3-dias-frozen-model-analog-smoke/outputs/per_frame_metrics.csv`
- `experiments/main/run-angiostress-s3-dias-frozen-model-analog-smoke/outputs/analog_summary.csv`
- `experiments/main/run-angiostress-s3-dias-frozen-model-analog-smoke/outputs/dias_s40_sam_overlay_panel.png`
- `CHECKLIST.md`
- `plan.md`
- `status.md`

## Evidence Paths

- `.ds/worktrees/run-angiostress-s3-dias-frozen-model-analog-smoke/experiments/main/run-angiostress-s3-dias-frozen-model-analog-smoke/RUN.md`
- `.ds/worktrees/run-angiostress-s3-dias-frozen-model-analog-smoke/experiments/main/run-angiostress-s3-dias-frozen-model-analog-smoke/VALIDATION.md`
- `.ds/worktrees/run-angiostress-s3-dias-frozen-model-analog-smoke/experiments/main/run-angiostress-s3-dias-frozen-model-analog-smoke/outputs/metrics_summary.json`
- `.ds/worktrees/run-angiostress-s3-dias-frozen-model-analog-smoke/experiments/main/run-angiostress-s3-dias-frozen-model-analog-smoke/outputs/per_frame_metrics.csv`
- `.ds/worktrees/run-angiostress-s3-dias-frozen-model-analog-smoke/experiments/main/run-angiostress-s3-dias-frozen-model-analog-smoke/outputs/analog_summary.csv`
- `.ds/worktrees/run-angiostress-s3-dias-frozen-model-analog-smoke/experiments/main/run-angiostress-s3-dias-frozen-model-analog-smoke/outputs/manifest.json`
- `.ds/worktrees/run-angiostress-s3-dias-frozen-model-analog-smoke/experiments/main/run-angiostress-s3-dias-frozen-model-analog-smoke/outputs/environment.json`
- `.ds/worktrees/run-angiostress-s3-dias-frozen-model-analog-smoke/experiments/main/run-angiostress-s3-dias-frozen-model-analog-smoke/outputs/dias_s40_sam_overlay_panel.png`

## Config Paths

- `.ds/worktrees/run-angiostress-s3-dias-frozen-model-analog-smoke/plan.md`
- `.ds/worktrees/run-angiostress-s3-dias-frozen-model-analog-smoke/CHECKLIST.md`

## Notes

- No model training or fine-tuning was performed.
- The frame-thinning and contrast-phase rows are deterministic summaries over retained-frame subsets after per-frame predictions, not a sequence-model perturbation study.
- DIAS s40 uses one sequence-level mask, so per-frame phase summaries are approximate and should not be overinterpreted.
- The label-derived bbox prompt is acceptable for harness feasibility but not a deployable perception setting.
- Device-overlay analogs remain deferred because CathAction data were source-audited but not locally loaded.

## Evaluation Summary

- Claim Update: Upgrade from real-data loader feasibility to real-data frozen-model metric feasibility. Do not upgrade to construct validity because there is one model, one sequence, no model ordering, and no synthetic-to-real rank correlation.
- Baseline Relation: The accepted TopCoW baseline remains the source/sanity comparator; S3 adds real DIAS evidence and is not a direct TopCoW-vs-DIAS score comparison.
- Failure Mode: SAM oversegments the DIAS s40 sequence under the label-derived bbox prompt, yielding low Dice and high component/area ratios; phase and thinning summaries are noisy because DIAS provides a sequence-level mask.
- Next Action: Run an explicit post-S3 decision and prioritize adding another frozen model or a model-panel ordering surface before claiming construct-validity readiness.

## Delivery Policy

- Research paper required: `True`
- Recommended next route: `revise_idea`
- Reason: Research paper mode is enabled, but the current run does not beat the baseline clearly enough. Revise the direction or strengthen the method before writing.
