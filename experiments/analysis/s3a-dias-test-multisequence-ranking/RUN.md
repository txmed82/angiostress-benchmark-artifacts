# s3a-dias-test-multisequence-ranking

## Objective

Expand the real-DIAS side of the S2c three-model frozen panel from one sequence to a deterministic labeled test-sequence subset, while preserving the frozen checkpoints, label-derived box prompt, and Dice/clDice metrics.

## Parent Evidence

- Parent run: `run-angiostress-s2c-third-frozen-model-panel-extension`
- Synthetic ordering source: `experiments/main/run-angiostress-s2c-third-frozen-model-panel-extension/outputs/model_summary.json`
- Selected DIAS test sequences: s40, s41, s42, s43, s44
- Claim boundary: diagnostic precursor only; no full construct-validity claim.

## Result

Synthetic stressor order: `['sam_vit_l', 'sam_vit_b', 'medsam_vit_b']`
DIAS multi-sequence order: `['medsam_vit_b', 'sam_vit_l', 'sam_vit_b']`

- Aggregate Spearman: `-0.5`
- Sequence-bootstrap Spearman mean: `-0.5000` with 95% CI `[-0.9000, 0.0000]`

## Model Summary

- medsam_vit_b: DIAS multi-sequence Dice 0.2531, clDice 0.2204, S2c synthetic stress Dice 0.2683
- sam_vit_b: DIAS multi-sequence Dice 0.2097, clDice 0.2364, S2c synthetic stress Dice 0.8926
- sam_vit_l: DIAS multi-sequence Dice 0.2204, clDice 0.2670, S2c synthetic stress Dice 0.9622

## Limitations

- DIAS provides sequence-level vessel labels, reused for each frame.
- The prompt remains an oracle label-derived bounding box, matching S2c and avoiding model tuning.
- The synthetic side is still one TopCoW case.
- CathAction/device-action analog coverage is still blocked by dataset access.
- The bootstrap interval resamples this small sequence subset and is not a final paper-level construct-validity interval.
