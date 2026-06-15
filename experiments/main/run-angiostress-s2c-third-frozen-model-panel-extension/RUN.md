# AngioStress S2c three-model frozen panel smoke

- Run id: `run-angiostress-s2c-third-frozen-model-panel-extension`
- Branch: `run/run-angiostress-s2c-third-frozen-model-panel-extension`
- Parent branch: `run/run-angiostress-s2b-frozen-model-panel-smoke`
- Worktree: `.ds/worktrees/run-run-angiostress-s2c-third-frozen-model-panel-extension`
- Idea: `idea-a229721e`
- Baseline: `angiostress-s0-topcow-resencm`
- Baseline variant: `one_case_topcow_resencm_1000ep`
- Dataset scope: `one deterministic topcow synthetic projection/stressor set and one dias test sequence s40 with sequence-level mask; no cathaction coverage in this run.`
- Verdict: `supported_for_three_model_panel_smoke_not_construct_validity`
- Status: `completed`

## Hypothesis

A third frozen public checkpoint-compatible model can be evaluated under the same synthetic TopCoW and DIAS s40 box-prompt protocol, enabling a three-model smoke ranking diagnostic without construct-validity claims.

## Setup

S2c extends the S2b SAM ViT-B and MedSAM ViT-B panel by adding official SAM ViT-L. All models are frozen and evaluated via segment_anything SamPredictor with identical label-derived bounding-box prompts.

## Execution

Compiled run_model_panel_smoke.py, ran a bounded tiny smoke, then ran the full S2c evaluator on 10 synthetic cells and 6 DIAS s40 frames per model. Full run bash id: bash-1a77a5a0; validation bash id: bash-88f8c924; branch commit: c6ffad2.

## Results

All three frozen models produced finite metrics. The synthetic mean stressor Dice order was SAM ViT-L > SAM ViT-B > MedSAM ViT-B, while DIAS mean Dice order was MedSAM ViT-B > SAM ViT-B > SAM ViT-L. The resulting smoke Spearman diagnostic was -1.0 with no confidence interval.

## Conclusion

Supported as a three-model frozen-panel smoke and a negative/discordant rank diagnostic. Do not upgrade to construct validity because this is one synthetic case, one DIAS sequence, no CathAction/device-action analog, and no confidence intervals.

## Metrics Summary

- `s2c_dias_frame_count_per_model` = 6
- `s2c_finite_metric_check` = 1
- `s2c_medsam_vit_b_dias_all_frame_mean_cldice` = 0.1389
- `s2c_medsam_vit_b_dias_all_frame_mean_dice` = 0.2139
- `s2c_medsam_vit_b_dias_contrast_phase_severity2_dice_delta_vs_severity0` = -0.0003
- `s2c_medsam_vit_b_dias_frame_thinning_severity2_dice_delta_vs_severity0` = 0.0015
- `s2c_medsam_vit_b_dias_min_frame_cldice` = 0.1087
- `s2c_medsam_vit_b_dias_min_frame_dice` = 0.2109
- `s2c_medsam_vit_b_dias_prediction_nonempty_rate` = 1
- `s2c_medsam_vit_b_synthetic_clean_cldice` = 0.2332
- `s2c_medsam_vit_b_synthetic_clean_dice` = 0.2554
- `s2c_medsam_vit_b_synthetic_mean_stressor_cldice` = 0.2479
- `s2c_medsam_vit_b_synthetic_mean_stressor_dice` = 0.2683
- `s2c_medsam_vit_b_synthetic_mean_stressor_dice_delta_vs_clean` = 0.0129
- `s2c_medsam_vit_b_synthetic_min_stressor_cldice` = 0.2238
- `s2c_medsam_vit_b_synthetic_min_stressor_dice` = 0.2448
- `s2c_model_count` = 3
- `s2c_ranked_model_count` = 3
- `s2c_sam_vit_b_dias_all_frame_mean_cldice` = 0.2345
- `s2c_sam_vit_b_dias_all_frame_mean_dice` = 0.2113
- `s2c_sam_vit_b_dias_contrast_phase_severity2_dice_delta_vs_severity0` = 0.0056
- `s2c_sam_vit_b_dias_frame_thinning_severity2_dice_delta_vs_severity0` = -0.0006
- `s2c_sam_vit_b_dias_min_frame_cldice` = 0.2065
- `s2c_sam_vit_b_dias_min_frame_dice` = 0.2057
- `s2c_sam_vit_b_dias_prediction_nonempty_rate` = 1
- `s2c_sam_vit_b_synthetic_clean_cldice` = 0.999
- `s2c_sam_vit_b_synthetic_clean_dice` = 0.981
- `s2c_sam_vit_b_synthetic_mean_stressor_cldice` = 0.9202
- `s2c_sam_vit_b_synthetic_mean_stressor_dice` = 0.8926
- `s2c_sam_vit_b_synthetic_mean_stressor_dice_delta_vs_clean` = -0.0884
- `s2c_sam_vit_b_synthetic_min_stressor_cldice` = 0.6425
- `s2c_sam_vit_b_synthetic_min_stressor_dice` = 0.5603
- `s2c_sam_vit_l_dias_all_frame_mean_cldice` = 0.2005
- `s2c_sam_vit_l_dias_all_frame_mean_dice` = 0.1792
- `s2c_sam_vit_l_dias_contrast_phase_severity2_dice_delta_vs_severity0` = 0.0106
- `s2c_sam_vit_l_dias_frame_thinning_severity2_dice_delta_vs_severity0` = 0.0001
- `s2c_sam_vit_l_dias_min_frame_cldice` = 0.1809
- `s2c_sam_vit_l_dias_min_frame_dice` = 0.1734
- `s2c_sam_vit_l_dias_prediction_nonempty_rate` = 1
- `s2c_sam_vit_l_synthetic_clean_cldice` = 0.9981
- `s2c_sam_vit_l_synthetic_clean_dice` = 0.9752
- `s2c_sam_vit_l_synthetic_mean_stressor_cldice` = 0.9661
- `s2c_sam_vit_l_synthetic_mean_stressor_dice` = 0.9622
- `s2c_sam_vit_l_synthetic_mean_stressor_dice_delta_vs_clean` = -0.013
- `s2c_sam_vit_l_synthetic_min_stressor_cldice` = 0.8493
- `s2c_sam_vit_l_synthetic_min_stressor_dice` = 0.9174
- `s2c_spearman_synthetic_mean_vs_dias_mean_dice` = -1
- `s2c_synthetic_item_count_per_model` = 10
- `s2c_total_prediction_count` = 48
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
- `s2c_dias_frame_count_per_model`: run=6 baseline=None delta=n/a (not comparable)
- `s2c_finite_metric_check`: run=1 baseline=None delta=n/a (not comparable)
- `s2c_medsam_vit_b_dias_all_frame_mean_cldice`: run=0.1389 baseline=None delta=n/a (not comparable)
- `s2c_medsam_vit_b_dias_all_frame_mean_dice`: run=0.2139 baseline=None delta=n/a (not comparable)
- `s2c_medsam_vit_b_dias_contrast_phase_severity2_dice_delta_vs_severity0`: run=-0.0003 baseline=None delta=n/a (not comparable)
- `s2c_medsam_vit_b_dias_frame_thinning_severity2_dice_delta_vs_severity0`: run=0.0015 baseline=None delta=n/a (not comparable)
- `s2c_medsam_vit_b_dias_min_frame_cldice`: run=0.1087 baseline=None delta=n/a (not comparable)
- `s2c_medsam_vit_b_dias_min_frame_dice`: run=0.2109 baseline=None delta=n/a (not comparable)
- `s2c_medsam_vit_b_dias_prediction_nonempty_rate`: run=1 baseline=None delta=n/a (not comparable)
- `s2c_medsam_vit_b_synthetic_clean_cldice`: run=0.2332 baseline=None delta=n/a (not comparable)
- `s2c_medsam_vit_b_synthetic_clean_dice`: run=0.2554 baseline=None delta=n/a (not comparable)
- `s2c_medsam_vit_b_synthetic_mean_stressor_cldice`: run=0.2479 baseline=None delta=n/a (not comparable)
- `s2c_medsam_vit_b_synthetic_mean_stressor_dice`: run=0.2683 baseline=None delta=n/a (not comparable)
- `s2c_medsam_vit_b_synthetic_mean_stressor_dice_delta_vs_clean`: run=0.0129 baseline=None delta=n/a (not comparable)
- `s2c_medsam_vit_b_synthetic_min_stressor_cldice`: run=0.2238 baseline=None delta=n/a (not comparable)
- `s2c_medsam_vit_b_synthetic_min_stressor_dice`: run=0.2448 baseline=None delta=n/a (not comparable)
- `s2c_model_count`: run=3 baseline=None delta=n/a (not comparable)
- `s2c_ranked_model_count`: run=3 baseline=None delta=n/a (not comparable)
- `s2c_sam_vit_b_dias_all_frame_mean_cldice`: run=0.2345 baseline=None delta=n/a (not comparable)
- `s2c_sam_vit_b_dias_all_frame_mean_dice`: run=0.2113 baseline=None delta=n/a (not comparable)
- `s2c_sam_vit_b_dias_contrast_phase_severity2_dice_delta_vs_severity0`: run=0.0056 baseline=None delta=n/a (not comparable)
- `s2c_sam_vit_b_dias_frame_thinning_severity2_dice_delta_vs_severity0`: run=-0.0006 baseline=None delta=n/a (not comparable)
- `s2c_sam_vit_b_dias_min_frame_cldice`: run=0.2065 baseline=None delta=n/a (not comparable)
- `s2c_sam_vit_b_dias_min_frame_dice`: run=0.2057 baseline=None delta=n/a (not comparable)
- `s2c_sam_vit_b_dias_prediction_nonempty_rate`: run=1 baseline=None delta=n/a (not comparable)
- `s2c_sam_vit_b_synthetic_clean_cldice`: run=0.999 baseline=None delta=n/a (not comparable)
- `s2c_sam_vit_b_synthetic_clean_dice`: run=0.981 baseline=None delta=n/a (not comparable)
- `s2c_sam_vit_b_synthetic_mean_stressor_cldice`: run=0.9202 baseline=None delta=n/a (not comparable)
- `s2c_sam_vit_b_synthetic_mean_stressor_dice`: run=0.8926 baseline=None delta=n/a (not comparable)
- `s2c_sam_vit_b_synthetic_mean_stressor_dice_delta_vs_clean`: run=-0.0884 baseline=None delta=n/a (not comparable)
- `s2c_sam_vit_b_synthetic_min_stressor_cldice`: run=0.6425 baseline=None delta=n/a (not comparable)
- `s2c_sam_vit_b_synthetic_min_stressor_dice`: run=0.5603 baseline=None delta=n/a (not comparable)
- `s2c_sam_vit_l_dias_all_frame_mean_cldice`: run=0.2005 baseline=None delta=n/a (not comparable)
- `s2c_sam_vit_l_dias_all_frame_mean_dice`: run=0.1792 baseline=None delta=n/a (not comparable)
- `s2c_sam_vit_l_dias_contrast_phase_severity2_dice_delta_vs_severity0`: run=0.0106 baseline=None delta=n/a (not comparable)
- `s2c_sam_vit_l_dias_frame_thinning_severity2_dice_delta_vs_severity0`: run=0.0001 baseline=None delta=n/a (not comparable)
- `s2c_sam_vit_l_dias_min_frame_cldice`: run=0.1809 baseline=None delta=n/a (not comparable)
- `s2c_sam_vit_l_dias_min_frame_dice`: run=0.1734 baseline=None delta=n/a (not comparable)
- `s2c_sam_vit_l_dias_prediction_nonempty_rate`: run=1 baseline=None delta=n/a (not comparable)
- `s2c_sam_vit_l_synthetic_clean_cldice`: run=0.9981 baseline=None delta=n/a (not comparable)
- `s2c_sam_vit_l_synthetic_clean_dice`: run=0.9752 baseline=None delta=n/a (not comparable)
- `s2c_sam_vit_l_synthetic_mean_stressor_cldice`: run=0.9661 baseline=None delta=n/a (not comparable)
- `s2c_sam_vit_l_synthetic_mean_stressor_dice`: run=0.9622 baseline=None delta=n/a (not comparable)
- `s2c_sam_vit_l_synthetic_mean_stressor_dice_delta_vs_clean`: run=-0.013 baseline=None delta=n/a (not comparable)
- `s2c_sam_vit_l_synthetic_min_stressor_cldice`: run=0.8493 baseline=None delta=n/a (not comparable)
- `s2c_sam_vit_l_synthetic_min_stressor_dice`: run=0.9174 baseline=None delta=n/a (not comparable)
- `s2c_spearman_synthetic_mean_vs_dias_mean_dice`: run=-1 baseline=None delta=n/a (not comparable)
- `s2c_synthetic_item_count_per_model`: run=10 baseline=None delta=n/a (not comparable)
- `s2c_total_prediction_count`: run=48 baseline=None delta=n/a (not comparable)

## Changed Files

- `CHECKLIST.md`
- `plan.md`
- `status.md`
- `experiments/main/run-angiostress-s2c-third-frozen-model-panel-extension/run_model_panel_smoke.py`
- `experiments/main/run-angiostress-s2c-third-frozen-model-panel-extension/model_candidate_audit.json`
- `experiments/main/run-angiostress-s2c-third-frozen-model-panel-extension/outputs/metrics_summary.json`
- `experiments/main/run-angiostress-s2c-third-frozen-model-panel-extension/outputs/model_summary.json`
- `experiments/main/run-angiostress-s2c-third-frozen-model-panel-extension/outputs/model_ranking_rows.json`
- `experiments/main/run-angiostress-s2c-third-frozen-model-panel-extension/RUN.md`
- `experiments/main/run-angiostress-s2c-third-frozen-model-panel-extension/VALIDATION.md`

## Evidence Paths

- `.ds/worktrees/run-run-angiostress-s2c-third-frozen-model-panel-extension/experiments/main/run-angiostress-s2c-third-frozen-model-panel-extension/outputs/metrics_summary.json`
- `.ds/worktrees/run-run-angiostress-s2c-third-frozen-model-panel-extension/experiments/main/run-angiostress-s2c-third-frozen-model-panel-extension/outputs/model_summary.json`
- `.ds/worktrees/run-run-angiostress-s2c-third-frozen-model-panel-extension/experiments/main/run-angiostress-s2c-third-frozen-model-panel-extension/outputs/model_ranking_rows.json`
- `.ds/worktrees/run-run-angiostress-s2c-third-frozen-model-panel-extension/experiments/main/run-angiostress-s2c-third-frozen-model-panel-extension/outputs/dias_per_frame_metrics.json`
- `.ds/worktrees/run-run-angiostress-s2c-third-frozen-model-panel-extension/experiments/main/run-angiostress-s2c-third-frozen-model-panel-extension/outputs/synthetic_per_cell_metrics.json`
- `.ds/worktrees/run-run-angiostress-s2c-third-frozen-model-panel-extension/experiments/main/run-angiostress-s2c-third-frozen-model-panel-extension/RUN.md`
- `.ds/worktrees/run-run-angiostress-s2c-third-frozen-model-panel-extension/experiments/main/run-angiostress-s2c-third-frozen-model-panel-extension/VALIDATION.md`

## Config Paths

- `.ds/worktrees/run-run-angiostress-s2c-third-frozen-model-panel-extension/experiments/main/run-angiostress-s2c-third-frozen-model-panel-extension/run_model_panel_smoke.py`
- `.ds/worktrees/run-run-angiostress-s2c-third-frozen-model-panel-extension/experiments/main/run-angiostress-s2c-third-frozen-model-panel-extension/model_candidate_audit.json`

## Notes

- No new model training, fine-tuning, or backbone modification was performed.
- SAM ViT-L checkpoint provenance is recorded in model_candidate_audit.json with official README/source URL, byte count, SHA256, and one-frame load/predict evidence.
- DIAS s40 uses a sequence-level mask and label-derived prompt box; this is an oracle-prompt benchmark smoke, not a deployable prompt protocol.
- The -1.0 Spearman value is a no-CI diagnostic over three models on one synthetic case and one DIAS sequence. It should be treated as discordant evidence, not a final construct-validity estimate.

## Evaluation Summary

- Claim Update: Upgrade from two-model panel feasibility to three-model panel feasibility; downgrade any readiness for construct-validity analysis because current ordering is fully discordant on one DIAS sequence.
- Next Action: Run decision stage. Likely next route is broader DIAS/CathAction coverage or device/action analog loading before paper-facing validity claims.

## Delivery Policy

- Research paper required: `True`
- Recommended next route: `revise_idea`
- Reason: Research paper mode is enabled, but the current run does not beat the baseline clearly enough. Revise the direction or strengthen the method before writing.
