# AngioStress S2 real-DSA loader and stressor-analog smoke

- Run id: `run-angiostress-s2-real-dsa-loader-smoke`
- Branch: `run/run-angiostress-s2-real-dsa-loader-smoke`
- Parent branch: `run/run-angiostress-s1-frozen-model-smoke`
- Worktree: `.ds/worktrees/run-angiostress-s2-real-dsa-loader-smoke`
- Idea: `idea-a229721e`
- Baseline: `angiostress-s0-topcow-resencm`
- Baseline variant: `one_case_topcow_resencm_1000ep`
- Dataset scope: `dias public zenodo archive metadata and local download; selected dias test sequence s40 with 6 frames and one sequence-level vessel mask. cathaction repository and project website were source-audited but local data were not loaded in this bounded run.`
- Verdict: `supported_for_dias_loader_feasibility_not_construct_validity`
- Status: `completed`

## Hypothesis

A trustworthy real-DSA intake path can be established from public DIAS data, with enough schema information to map frame thinning and contrast-phase analogs for later synthetic-to-real construct-validity testing.

## Setup

Used the active run worktree run/run-angiostress-s2-real-dsa-loader-smoke. Shallow-cloned DIAS and CathAction repositories into quest tmp for schema inspection. Downloaded DIAS.zip from Zenodo and verified it against the published md5 checksum before building the loader manifest.

## Execution

Parsed the DIAS zip inventory, derived sequence split counts, extracted DIAS test sequence s40 frames plus label, rendered a preview overlay, wrote real_dsa_loader_manifest.json, and validated required evidence files, sample extraction, checksum status, frame counts, label area, and analog status fields.

## Results

DIAS.zip md5 matched the published checksum. The archive contains 60 sequences: 30 training, 10 validation, and 20 test. Selected sequence s40 has 6 extracted 800 x 800 frames and a sequence-level mask with 71,224 nonzero pixels. Frame thinning and contrast-phase analogs are immediately available from DIAS sequence frames. Device-overlay analogs are not available from DIAS alone; CathAction is source-audited but local data loading remains deferred behind the dataset download/license flow.

## Conclusion

The real-DSA loader smoke is supported for DIAS: AngioStress now has a verified public real-angiography source, a reproducible sample manifest, and two real stressor analog families ready for the next frozen-model real-data smoke. This is still not a construct-validity estimate because model failure ordering and synthetic-to-real rank correlation have not been measured.

## Metrics Summary

- `topcow_resencm_one_case_mean_dice` = 0.6985
- `topcow_resencm_one_case_mean_cldice` = 0.6285
- `topcow_resencm_one_case_graph_ready_rate` = 1
- `topcow_gt_sanity_mean_dice` = 1
- `topcow_gt_sanity_mean_cldice` = 1
- `topcow_gt_sanity_graph_ready_rate` = 1
- `dias_archive_md5_matches_published` = 1
- `dias_sequence_count` = 60
- `dias_training_sequence_count` = 30
- `dias_validation_sequence_count` = 10
- `dias_test_sequence_count` = 20
- `dias_selected_s40_frame_count` = 6
- `dias_selected_s40_label_nonzero_pixels` = 71224
- `dias_frame_thinning_analog_available` = 1
- `dias_contrast_phase_analog_available` = 1
- `dias_device_overlay_analog_available` = 0
- `cathaction_source_audited` = 1
- `cathaction_local_data_loaded` = 0

## Baseline Comparison

- `topcow_resencm_one_case_mean_dice`: run=0.6985 baseline=0.6985 delta=0 (worse)
- `topcow_resencm_one_case_mean_cldice`: run=0.6285 baseline=0.6285 delta=0 (worse)
- `topcow_resencm_one_case_graph_ready_rate`: run=1 baseline=1 delta=0 (worse)
- `topcow_gt_sanity_mean_dice`: run=1 baseline=1 delta=0 (worse)
- `topcow_gt_sanity_mean_cldice`: run=1 baseline=1 delta=0 (worse)
- `topcow_gt_sanity_graph_ready_rate`: run=1 baseline=1 delta=0 (worse)
- `topcow_resencm_checkpoint_train_mean_dice`: run=None baseline=0.7261 delta=n/a (not comparable)
- `dias_archive_md5_matches_published`: run=1 baseline=None delta=n/a (not comparable)
- `dias_sequence_count`: run=60 baseline=None delta=n/a (not comparable)
- `dias_training_sequence_count`: run=30 baseline=None delta=n/a (not comparable)
- `dias_validation_sequence_count`: run=10 baseline=None delta=n/a (not comparable)
- `dias_test_sequence_count`: run=20 baseline=None delta=n/a (not comparable)
- `dias_selected_s40_frame_count`: run=6 baseline=None delta=n/a (not comparable)
- `dias_selected_s40_label_nonzero_pixels`: run=71224 baseline=None delta=n/a (not comparable)
- `dias_frame_thinning_analog_available`: run=1 baseline=None delta=n/a (not comparable)
- `dias_contrast_phase_analog_available`: run=1 baseline=None delta=n/a (not comparable)
- `dias_device_overlay_analog_available`: run=0 baseline=None delta=n/a (not comparable)
- `cathaction_source_audited`: run=1 baseline=None delta=n/a (not comparable)
- `cathaction_local_data_loaded`: run=0 baseline=None delta=n/a (not comparable)

## Changed Files

- `plan.md`
- `PLAN.md`
- `CHECKLIST.md`
- `status.md`
- `experiments/main/run-angiostress-s2-real-dsa-loader-smoke/RUN.md`
- `experiments/main/run-angiostress-s2-real-dsa-loader-smoke/VALIDATION.md`
- `experiments/main/run-angiostress-s2-real-dsa-loader-smoke/build_dias_loader_manifest.py`
- `experiments/main/run-angiostress-s2-real-dsa-loader-smoke/source_availability_audit.json`
- `experiments/main/run-angiostress-s2-real-dsa-loader-smoke/repo_schema_audit.json`
- `experiments/main/run-angiostress-s2-real-dsa-loader-smoke/cathaction_website_audit.json`
- `experiments/main/run-angiostress-s2-real-dsa-loader-smoke/dias_zip_inventory.json`
- `experiments/main/run-angiostress-s2-real-dsa-loader-smoke/dias_sequence_inventory.json`
- `experiments/main/run-angiostress-s2-real-dsa-loader-smoke/metrics_summary.json`
- `experiments/main/run-angiostress-s2-real-dsa-loader-smoke/outputs/real_dsa_loader_manifest.json`
- `experiments/main/run-angiostress-s2-real-dsa-loader-smoke/outputs/dias_s40_preview.png`

## Evidence Paths

- `experiments/main/run-angiostress-s2-real-dsa-loader-smoke/RUN.md`
- `experiments/main/run-angiostress-s2-real-dsa-loader-smoke/VALIDATION.md`
- `experiments/main/run-angiostress-s2-real-dsa-loader-smoke/build_dias_loader_manifest.py`
- `experiments/main/run-angiostress-s2-real-dsa-loader-smoke/source_availability_audit.json`
- `experiments/main/run-angiostress-s2-real-dsa-loader-smoke/repo_schema_audit.json`
- `experiments/main/run-angiostress-s2-real-dsa-loader-smoke/cathaction_website_audit.json`
- `experiments/main/run-angiostress-s2-real-dsa-loader-smoke/dias_zip_inventory.json`
- `experiments/main/run-angiostress-s2-real-dsa-loader-smoke/dias_sequence_inventory.json`
- `experiments/main/run-angiostress-s2-real-dsa-loader-smoke/metrics_summary.json`
- `experiments/main/run-angiostress-s2-real-dsa-loader-smoke/outputs/real_dsa_loader_manifest.json`
- `experiments/main/run-angiostress-s2-real-dsa-loader-smoke/outputs/dias_s40_preview.png`

## Config Paths

- `experiments/main/run-angiostress-s2-real-dsa-loader-smoke/build_dias_loader_manifest.py`

## Notes

- DIAS labels are sequence-level masks named label_sXX.png, while frames are image_sXX_iYY.png.
- The selected sample preview was inspected and is nonblank with mask overlay aligned to the visible vessel tree.
- CathAction remains important for device-overlay analogs, but local data loading is deferred because the dataset requires its download/license path.

## Evaluation Summary

- Not recorded.

## Delivery Policy

- Research paper required: `True`
- Recommended next route: `revise_idea`
- Reason: Research paper mode is enabled, but the current run does not beat the baseline clearly enough. Revise the direction or strengthen the method before writing.
