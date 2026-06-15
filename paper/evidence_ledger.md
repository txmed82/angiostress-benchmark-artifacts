# Evidence Ledger

- Selected outline: `outline-001`
- Paper line: `paper-run-angiostress-s2c-third-frozen-model-panel-extension-outline-001-run-angiostress-s2c-third-frozen-model-panel-extension`
- Updated at: 2026-06-15T04:10:38.584Z

## run-angiostress-s0s1-renderer-smoke
- Title: AngioStress S0/S1 renderer-smoke benchmark artifact
- Status: completed
- Section: main-results
- Paper role: main_text
- Claims: -
- Result: The renderer-smoke pass generated 9 stressor cells across frame thinning, contrast phase, and device overlay. Required outputs were present; the projected GT area was 8,233 pixels with 2 connected components; clean GT self Dice and self clDice were both 1.0; all numeric metrics were finite; fresh rerun output hashes and per-cell hashes matched. Frozen 2D model inference was not run in this scoped pass and is recorded as deferred.

## run-angiostress-s1-frozen-model-smoke
- Title: AngioStress S1 frozen-model harness smoke with SAM ViT-B
- Status: completed
- Section: main-results
- Paper role: main_text
- Claims: -
- Result: SAM ViT-B produced 10 prediction rows and 10 mask PNG/NPY outputs. Clean Dice was 0.9810482128526452 and clean clDice was 0.9990412272291467. Across 9 stressed cells, mean Dice was 0.892633475863582 and mean clDice was 0.920166815700077. Mean Dice delta vs clean was -0.08841473698906317. Device overlay was the strongest observed degradation family: mean Dice 0.7218091541803723, mean clDice 0.76477019540269. The strongest single cell was device_overlay_severity_2 with Dice 0.6241094597782496, clDice 0.6424506218998289, and component-count ratio 66.0.

## run-angiostress-s2-real-dsa-loader-smoke
- Title: AngioStress S2 real-DSA loader and stressor-analog smoke
- Status: completed
- Section: main-results
- Paper role: main_text
- Claims: -
- Result: DIAS.zip md5 matched the published checksum. The archive contains 60 sequences: 30 training, 10 validation, and 20 test. Selected sequence s40 has 6 extracted 800 x 800 frames and a sequence-level mask with 71,224 nonzero pixels. Frame thinning and contrast-phase analogs are immediately available from DIAS sequence frames. Device-overlay analogs are not available from DIAS alone; CathAction is source-audited but local data loading remains deferred behind the dataset download/license flow.

## run-angiostress-s2b-frozen-model-panel-smoke
- Title: Frozen-model panel smoke on shared AngioStress synthetic and DIAS surfaces
- Status: completed
- Section: main-results
- Paper role: main_text
- Claims: -
- Result: The two-model panel is measurable and rankable, but the initial ordering is discordant across surfaces. SAM ViT-B is much stronger on the synthetic stressor surface (mean stressor Dice 0.8926 vs MedSAM 0.2683), while MedSAM is only slightly higher than SAM on DIAS mean Dice (0.2139 vs 0.2113). The run records this as a panel-smoke result, not as construct validity.

## run-angiostress-s2c-third-frozen-model-panel-extension
- Title: AngioStress S2c three-model frozen panel smoke
- Status: completed
- Section: main-results
- Paper role: main_text
- Claims: -
- Result: All three frozen models produced finite metrics. The synthetic mean stressor Dice order was SAM ViT-L > SAM ViT-B > MedSAM ViT-B, while DIAS mean Dice order was MedSAM ViT-B > SAM ViT-B > SAM ViT-L. The resulting smoke Spearman diagnostic was -1.0 with no confidence interval.

## run-angiostress-s3-dias-frozen-model-analog-smoke
- Title: DIAS Frozen SAM Real-Analog Smoke
- Status: completed
- Section: main-results
- Paper role: main_text
- Claims: -
- Result: The run produced finite per-frame and per-analog metrics, prediction masks, overlays, and validation records. SAM predicted nonempty masks for all 6 frames, but performance was weak under the label-derived bbox prompt: all-frame mean Dice 0.21131857528530187 and mean clDice 0.2344899136404658. Frame-thinning severity 2 had Dice delta -0.0005932835787929025 versus severity 0; contrast-phase severity 2 had Dice delta 0.0056035950660932865 versus severity 0. These are real-side harness feasibility results, not construct-validity estimates.

## analysis-s3b-dias-full-test-ranking
- Title: S3b full DIAS frozen-panel ranking diagnostic
- Status: completed
- Section: main-results
- Paper role: main_text
- Claims: `C2`, `C3`
- Result: Full-DIAS ranking covers 20 test sequences, 115 frames per model, and 345 frozen-model predictions. Mean Dice order is MedSAM ViT-B > SAM ViT-L > SAM ViT-B, with means 0.2953272961, 0.2628457985, and 0.2404712606. Relative to the S2c synthetic mean-stressor order, aggregate Spearman is -0.5, aggregate Kendall is -0.3333333333, and sequence-bootstrap Spearman mean is -0.425 with 95% CI [-0.675, -0.125]. This is discordant real-surface rank evidence, not a positive construct-validity claim.

## analysis-s3f-cathaction-human-segmentation-subset-ranking
- Title: S3f CathAction human-segmentation subset ranking diagnostic
- Status: completed
- Section: main-results
- Paper role: main_text
- Claims: `C2`, `C3`
- Result: CathAction ranking covers 128 nonempty pairs per model and 384 frozen-model predictions. Mean Dice order is SAM ViT-B > SAM ViT-L > MedSAM ViT-B, with means 0.3647474714, 0.3463619310, and 0.0997291104; mean clDice values are 0.4022584582, 0.3642721988, and 0.0870552374. Relative to the S2c synthetic mean-stressor order, Spearman is 0.5 and fixed-subset bootstrap Spearman mean is 0.5285 with percentile interval [0.5, 1.0]. The observed-order match rate is 0.943 and the synthetic-order match rate is 0.057, supporting partial agreement mainly through stable MedSAM-last behavior with a SAM ViT-B/SAM ViT-L swap.
