# S3e CathAction Human Segmentation Panel Smoke

## Identity

- run_id: `s3e-cathaction-human-segmentation-panel-smoke`
- parent_run_id: `run-angiostress-s2c-third-frozen-model-panel-extension`
- route_decision: `decision-de02d4de`
- storage_decision: `decision-06a3b189`
- command: `experiments/analysis/s3e-cathaction-human-segmentation-panel-smoke/run_cathaction_human_segmentation_smoke.py --zip-path tmp/cathaction_s3e/segmentation_human_train.zip --out experiments/analysis/s3e-cathaction-human-segmentation-panel-smoke/outputs --workspace-root .ds/worktrees/run-run-angiostress-s2c-third-frozen-model-panel-extension --device auto --sample-count 8 --delete-zip-after-run`
- device: `mps`

## Inputs

- CathAction retained zip: `gs://seldinger-datasets-raw/angiostress/cathaction/hf/segmentation_human_train.zip`
- Local zip path during run: `tmp/cathaction_s3e/segmentation_human_train.zip`
- Local zip source sha256: `087c8f971e0455ad67d092a944df75ee7244cbead10e1091c26046ea271e2cf5`
- Sample count per model: `8`
- Pair selection: deterministic evenly spaced index selection over the 5,283 paired records.
- Model panel: SAM ViT-B, MedSAM ViT-B, and SAM ViT-L, all frozen.

## Method

The runner imports the S2c frozen-panel helpers for checkpoint verification, SAM predictor construction, bbox prompting, Dice/clDice, and overlay rendering. It reads sampled JPG/PNG pairs directly from the zip into memory without extracting the archive. Prompts are CathAction mask-derived bounding boxes for measurement plumbing only.

## Claim Boundary

This is a bounded CathAction segmentation smoke. It checks whether the frozen panel can be evaluated on a small CathAction human-segmentation sample and gives a rank-order diagnostic. It does not estimate synthetic-to-real construct validity, confidence intervals, or clinical accuracy.
