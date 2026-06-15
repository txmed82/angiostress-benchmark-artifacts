# AngioStress S0/S1 TopCoW-ResEncM Baseline

## Verdict

- Baseline id: `angiostress-s0-topcow-resencm`
- Variant: `one_case_topcow_resencm_1000ep`
- Route: `verify-local-existing`
- Acceptance target: `comparison_ready`
- Verification verdict: `trusted_with_caveats`

This baseline confirms a narrow local source-and-sanity comparator for AngioStress S0/S1: one concrete TopCoW CTA Circle-of-Willis case with readable voxel-level labels, plus an existing frozen 3D nnU-Net/ResidualEncoder sanity evaluation. It is enough to unblock the first deterministic projection and benchmark-harness direction.

It is not a DIAS/CathAction real-DSA frozen-model baseline and must not be used as evidence for synthetic-to-real construct validity.

## Verified Local Assets

- TopCoW one-case manifest: `external/topcow-baseline/seldinger-ml/outputs/topcow_local_one_case_manifest.jsonl`
- Case id: `topcow_CTA_ISLES2024_TUM_sub-stroke_0002_ct`
- Volume: `tmp/topcow/source_case/volume.nii.gz`
- Volume SHA256: `c04f8897330454b585fcfc96b053fb45ae4dacf474a2211cc7c5da9fb47f3bdb`
- Mask: `tmp/topcow/source_case/named.nii.gz`
- Mask SHA256: `8af198d6f7bf97cbedb0bb6ce510982645a9d7de52366f610271e1981405b1e4`
- Shape: `229 x 279 x 371`
- Spacing: `0.607422 x 0.607422 x 0.399998`

## Trusted Reports

- GT sanity report: `external/topcow-baseline/seldinger-ml/outputs/topcow_gt_mask_sanity_eval.json`
- GT sanity report SHA256: `119800640d4ba10c7c2e495b1284d8978bdb8969ed05fe1022f0f92c097a5158`
- Frozen ResEncM report: `external/topcow-baseline/seldinger-ml/outputs/topcow_resencm_1000ep_eval.json`
- Frozen ResEncM report SHA256: `20c54c9bd7ecba2487da47eabaa37b69fa720efff0e6cb84bf85267888372ea6`
- Frozen checkpoint: `/tmp/seldinger_models/resencm_1000ep_fold0/checkpoint_best.pth`
- Frozen checkpoint SHA256: `49907637a92058c16ac8249835864ff251f214c2b6052f849f9a34104f29f723`

## Core Metrics

- `topcow_resencm_one_case_mean_dice`: `0.6984658547796687`
- `topcow_resencm_one_case_mean_cldice`: `0.6285484218960072`
- `topcow_resencm_one_case_graph_ready_rate`: `1.0`
- `topcow_gt_sanity_mean_dice`: `1.0`
- `topcow_gt_sanity_mean_cldice`: `1.0`
- `topcow_gt_sanity_graph_ready_rate`: `1.0`

## Caveats

- The verified source case is CTA TopCoW, not DSA.
- The frozen metric is a 3D source-label sanity comparator, not a 2D projection or DIAS/CathAction perception model.
- The one-case ResEncM metric is sufficient only for S0/S1 bootstrap and route selection. Paper-facing construct-validity claims require later DIAS/CathAction loading, frozen 2D/sequence model evaluation, and synthetic-to-real correlation estimates with confidence intervals.
- The checkpoint currently lives under `/tmp/seldinger_models/resencm_1000ep_fold0`; reverify or copy/register it before relying on it for long-lived external release.

## Next Anchor

Leave baseline after artifact confirmation and enter `idea`: choose the first AngioStress implementation direction around deterministic TopCoW clean projection, GT-format preservation, DIAS/CathAction loading plan, and one frozen model smoke path.
