# s3b-dias-full-test-split-ranking

## Objective

Expand the real-DIAS side of the S2c three-model frozen panel from one sequence to a deterministic labeled test-sequence subset, while preserving the frozen checkpoints, label-derived box prompt, and Dice/clDice metrics.

## Parent Evidence

- Parent run: `run-angiostress-s2c-third-frozen-model-panel-extension`
- Synthetic ordering source: `experiments/main/run-angiostress-s2c-third-frozen-model-panel-extension/outputs/model_summary.json`
- Selected DIAS test sequences: s40, s41, s42, s43, s44, s45, s46, s47, s48, s49, s50, s51, s52, s53, s54, s55, s56, s57, s58, s59
- Claim boundary: diagnostic precursor only; no full construct-validity claim.

## Result

Synthetic stressor order: `['sam_vit_l', 'sam_vit_b', 'medsam_vit_b']`
DIAS multi-sequence order: `['medsam_vit_b', 'sam_vit_l', 'sam_vit_b']`

- Aggregate Spearman: `-0.5`
- Sequence-bootstrap Spearman mean: `-0.4250` with 95% CI `[-0.6750, -0.1250]`

## Model Summary

- medsam_vit_b: DIAS multi-sequence Dice 0.2953, clDice 0.2717, S2c synthetic stress Dice 0.2683
- sam_vit_b: DIAS multi-sequence Dice 0.2405, clDice 0.2391, S2c synthetic stress Dice 0.8926
- sam_vit_l: DIAS multi-sequence Dice 0.2628, clDice 0.2691, S2c synthetic stress Dice 0.9622

## Limitations

- DIAS provides sequence-level vessel labels, reused for each frame.
- The prompt remains an oracle label-derived bounding box, matching S2c and avoiding model tuning.
- The synthetic side is still one TopCoW case.
- CathAction/device-action analog coverage is still blocked by dataset access.
- The bootstrap interval resamples this small sequence subset and is not a final paper-level construct-validity interval.
