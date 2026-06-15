# Frozen-model panel smoke on shared AngioStress synthetic and DIAS surfaces

- Run id: `run-angiostress-s2b-frozen-model-panel-smoke`
- Branch: `run/run-angiostress-s2b-frozen-model-panel-smoke`
- Parent branch: `run/run-angiostress-s3-dias-frozen-model-analog-smoke`
- Worktree: `.ds/worktrees/run-angiostress-s2b-frozen-model-panel-smoke`
- Idea: `idea-a229721e`
- Baseline: `angiostress-s0-topcow-resencm`
- Baseline variant: `one_case_topcow_resencm_1000ep`
- Dataset scope: `one deterministic topcow-derived synthetic case with clean plus 9 stressor cells, and one verified dias test sequence s40 with 6 frames and a sequence-level mask. cathaction/device-overlay real analogs remain deferred.`
- Verdict: `supported_for_panel_smoke_not_construct_validity`
- Status: `completed`

## Hypothesis

A second frozen public SAM-style model can be evaluated on the same deterministic synthetic stressor cells and verified DIAS s40 frames, producing finite comparable model-ordering rows before any construct-validity claim is attempted.

## Setup

SAM ViT-B and MedSAM ViT-B were evaluated frozen through segment_anything SamPredictor. MedSAM used the official README-linked checkpoint with a local CPU-mapped copy because the original file is CUDA-serialized. Both models used identical label-derived bounding-box prompts for the TopCoW synthetic projection and the DIAS s40 sequence-level mask.

## Execution

Committed evaluator/output commit eacf224. Full command: python experiments/main/run-angiostress-s2b-frozen-model-panel-smoke/run_model_panel_smoke.py --out experiments/main/run-angiostress-s2b-frozen-model-panel-smoke/outputs --device auto. Device selected by the evaluator: mps. Validation confirmed 2 model summaries, 20 synthetic rows, 12 DIAS frame rows, 12 DIAS analog rows, 10 ranking rows, and finite metrics.

## Results

The two-model panel is measurable and rankable, but the initial ordering is discordant across surfaces. SAM ViT-B is much stronger on the synthetic stressor surface (mean stressor Dice 0.8926 vs MedSAM 0.2683), while MedSAM is only slightly higher than SAM on DIAS mean Dice (0.2139 vs 0.2113). The run records this as a panel-smoke result, not as construct validity.

## Conclusion

Supported as a frozen-model panel smoke: AngioStress now evaluates two frozen public models on shared synthetic and DIAS surfaces and emits finite model-ordering rows. Do not upgrade to construct validity because there are only two models, one synthetic case, one DIAS sequence, no confidence interval, no CathAction/device-overlay real analog, and the surface ordering is discordant in this initial smoke.

## Metrics Summary

- `topcow_resencm_one_case_mean_dice` = 0.6985
- `topcow_resencm_one_case_mean_cldice` = 0.6285
- `topcow_resencm_one_case_graph_ready_rate` = 1
- `topcow_gt_sanity_mean_dice` = 1
- `topcow_gt_sanity_mean_cldice` = 1
- `topcow_gt_sanity_graph_ready_rate` = 1
- `s2b_model_count` = 2
- `s2b_synthetic_item_count_per_model` = 10
- `s2b_dias_frame_count_per_model` = 6
- `s2b_total_prediction_count` = 32
- `s2b_ranked_model_count` = 2
- `s2b_finite_metric_check` = 1
- `s2b_two_model_order_agreement_synthetic_mean_vs_dias` = -1
- `s2b_sam_vit_b_synthetic_clean_dice` = 0.981
- `s2b_sam_vit_b_synthetic_mean_stressor_dice` = 0.8926
- `s2b_sam_vit_b_synthetic_mean_stressor_dice_delta_vs_clean` = -0.0884
- `s2b_sam_vit_b_dias_all_frame_mean_dice` = 0.2113
- `s2b_sam_vit_b_dias_all_frame_mean_cldice` = 0.2345
- `s2b_sam_vit_b_dias_frame_thinning_severity2_dice_delta_vs_severity0` = -0.0006
- `s2b_sam_vit_b_dias_contrast_phase_severity2_dice_delta_vs_severity0` = 0.0056
- `s2b_medsam_vit_b_synthetic_clean_dice` = 0.2554
- `s2b_medsam_vit_b_synthetic_mean_stressor_dice` = 0.2683
- `s2b_medsam_vit_b_synthetic_mean_stressor_dice_delta_vs_clean` = 0.0129
- `s2b_medsam_vit_b_dias_all_frame_mean_dice` = 0.2139
- `s2b_medsam_vit_b_dias_all_frame_mean_cldice` = 0.1389
- `s2b_medsam_vit_b_dias_frame_thinning_severity2_dice_delta_vs_severity0` = 0.0015
- `s2b_medsam_vit_b_dias_contrast_phase_severity2_dice_delta_vs_severity0` = -0.0003

## Baseline Comparison

- `topcow_resencm_one_case_mean_dice`: run=0.6985 baseline=0.6985 delta=0 (worse)
- `topcow_resencm_one_case_mean_cldice`: run=0.6285 baseline=0.6285 delta=0 (worse)
- `topcow_resencm_one_case_graph_ready_rate`: run=1 baseline=1 delta=0 (worse)
- `topcow_gt_sanity_mean_dice`: run=1 baseline=1 delta=0 (worse)
- `topcow_gt_sanity_mean_cldice`: run=1 baseline=1 delta=0 (worse)
- `topcow_gt_sanity_graph_ready_rate`: run=1 baseline=1 delta=0 (worse)
- `topcow_resencm_checkpoint_train_mean_dice`: run=None baseline=0.7261 delta=n/a (not comparable)
- `s2b_model_count`: run=2 baseline=None delta=n/a (not comparable)
- `s2b_synthetic_item_count_per_model`: run=10 baseline=None delta=n/a (not comparable)
- `s2b_dias_frame_count_per_model`: run=6 baseline=None delta=n/a (not comparable)
- `s2b_total_prediction_count`: run=32 baseline=None delta=n/a (not comparable)
- `s2b_ranked_model_count`: run=2 baseline=None delta=n/a (not comparable)
- `s2b_finite_metric_check`: run=1 baseline=None delta=n/a (not comparable)
- `s2b_two_model_order_agreement_synthetic_mean_vs_dias`: run=-1 baseline=None delta=n/a (not comparable)
- `s2b_sam_vit_b_synthetic_clean_dice`: run=0.981 baseline=None delta=n/a (not comparable)
- `s2b_sam_vit_b_synthetic_mean_stressor_dice`: run=0.8926 baseline=None delta=n/a (not comparable)
- `s2b_sam_vit_b_synthetic_mean_stressor_dice_delta_vs_clean`: run=-0.0884 baseline=None delta=n/a (not comparable)
- `s2b_sam_vit_b_dias_all_frame_mean_dice`: run=0.2113 baseline=None delta=n/a (not comparable)
- `s2b_sam_vit_b_dias_all_frame_mean_cldice`: run=0.2345 baseline=None delta=n/a (not comparable)
- `s2b_sam_vit_b_dias_frame_thinning_severity2_dice_delta_vs_severity0`: run=-0.0006 baseline=None delta=n/a (not comparable)
- `s2b_sam_vit_b_dias_contrast_phase_severity2_dice_delta_vs_severity0`: run=0.0056 baseline=None delta=n/a (not comparable)
- `s2b_medsam_vit_b_synthetic_clean_dice`: run=0.2554 baseline=None delta=n/a (not comparable)
- `s2b_medsam_vit_b_synthetic_mean_stressor_dice`: run=0.2683 baseline=None delta=n/a (not comparable)
- `s2b_medsam_vit_b_synthetic_mean_stressor_dice_delta_vs_clean`: run=0.0129 baseline=None delta=n/a (not comparable)
- `s2b_medsam_vit_b_dias_all_frame_mean_dice`: run=0.2139 baseline=None delta=n/a (not comparable)
- `s2b_medsam_vit_b_dias_all_frame_mean_cldice`: run=0.1389 baseline=None delta=n/a (not comparable)
- `s2b_medsam_vit_b_dias_frame_thinning_severity2_dice_delta_vs_severity0`: run=0.0015 baseline=None delta=n/a (not comparable)
- `s2b_medsam_vit_b_dias_contrast_phase_severity2_dice_delta_vs_severity0`: run=-0.0003 baseline=None delta=n/a (not comparable)

## Changed Files

- `CHECKLIST.md`
- `experiments/main/run-angiostress-s2b-frozen-model-panel-smoke`

## Evidence Paths

- `experiments/main/run-angiostress-s2b-frozen-model-panel-smoke/model_candidate_audit.json`
- `experiments/main/run-angiostress-s2b-frozen-model-panel-smoke/run_model_panel_smoke.py`
- `experiments/main/run-angiostress-s2b-frozen-model-panel-smoke/outputs/metrics_summary.json`
- `experiments/main/run-angiostress-s2b-frozen-model-panel-smoke/outputs/model_summary.json`
- `experiments/main/run-angiostress-s2b-frozen-model-panel-smoke/outputs/model_ranking_rows.json`
- `experiments/main/run-angiostress-s2b-frozen-model-panel-smoke/outputs/synthetic_per_cell_metrics.json`
- `experiments/main/run-angiostress-s2b-frozen-model-panel-smoke/outputs/dias_per_frame_metrics.json`
- `experiments/main/run-angiostress-s2b-frozen-model-panel-smoke/outputs/dias_analog_summary.json`
- `experiments/main/run-angiostress-s2b-frozen-model-panel-smoke/VALIDATION.md`

## Config Paths

- `experiments/main/run-angiostress-s2b-frozen-model-panel-smoke/run_model_panel_smoke.py`
- `experiments/main/run-angiostress-s2b-frozen-model-panel-smoke/model_candidate_audit.json`

## Notes

- MedSAM was used only as a frozen public checkpoint; no training or fine-tuning was performed.
- The official MedSAM checkpoint was CPU-mapped locally for non-CUDA loading; original and CPU-copy SHA256 values are recorded in model_candidate_audit.json.
- DIAS s40 uses a sequence-level mask, so frame-level phase analog summaries remain approximate.
- This result must not be described as clinical accuracy, sim-to-real transfer, or construct validity.

## Evaluation Summary

- Claim Update: Upgrade from one-model real-DIAS harness feasibility to two-model frozen panel feasibility. Do not upgrade to construct validity.
- Next Action: Run a post-S2b decision. The likely next route is to add at least one more frozen model or expand DIAS/CathAction analog coverage before paper-facing construct-validity analysis.

## Delivery Policy

- Research paper required: `True`
- Recommended next route: `revise_idea`
- Reason: Research paper mode is enabled, but the current run does not beat the baseline clearly enough. Revise the direction or strengthen the method before writing.
