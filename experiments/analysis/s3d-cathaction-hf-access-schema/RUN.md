# S3d CathAction HF Access Schema Validation

## Objective

Validate the Hugging Face CathAction access route and inspect the smallest relevant segmentation archive without a full local dataset pull.

## Parent

- Parent run: `run-angiostress-s2c-third-frozen-model-panel-extension`
- Route decision: `decision-289478b1`
- Superseded fallback: `decision-b14faaa3`

## HF Dataset Metadata

- Dataset: `airvlab/CathAction`
- SHA: `8b04056f0f4fa4b04d8454728f000730af0d5560`
- License tag: `cc-by-nc-sa-4.0`
- HF metadata gated/private: `false` / `false`
- Total compressed payload estimate: about 52.3 GiB

Payloads checked by metadata/HEAD only:

- `segmentation_human_train.zip`: 0.133 GiB, used for S3d schema validation
- `collision_detection.zip`: 4.051 GiB, deferred
- `segmentation_animal_phantom.zip`: 9.204 GiB, deferred
- `video_action_understanding.zip`: 38.937 GiB, deferred

## Storage Envelope

Local disk had about 162 GiB free at the check. The first `gcloud` check used the wrong Python runtime, so the earlier "GCP unavailable" note was downgraded to an environment issue. With `CLOUDSDK_PYTHON=/opt/homebrew/bin/python3`, the Cloud SDK sees project `agile-athlete-496814-s6`, account `colin@seldinger.med`, and buckets `seldinger-datasets-raw`, `seldinger-datasets-curated`, and `seldinger-tfstate`.

The small human segmentation archive is now retained at `gs://seldinger-datasets-raw/angiostress/cathaction/hf/segmentation_human_train.zip` as a 143,049,194-byte object. The temporary local upload copy was deleted after verification.

## Result

The small human segmentation archive is accessible and schema-usable. It contains 5,283 JPG images and 5,283 PNG masks under `human_dataset_train/img` and `human_dataset_train/mask`. Pairing succeeds after stripping the `_mask` suffix from mask basenames: 5,283/5,283 image-mask pairs, with 0 unmatched images and 0 unmatched masks. A 20-pair in-memory sample had 512 x 512 image/mask dimensions and binary mask extrema `(0, 255)`.

## Claim Boundary

This is access/schema evidence only. It does not measure frozen-model performance and does not support a CathAction construct-validity claim yet.
