# Validation

## Checks

- outputs_exist: true
- finite_metric_check: `1.0`
- model_count: `3.0`
- sample_count_per_model: `8.0`
- total_prediction_count: `24.0`
- local_zip_exists_after_cleanup: `False`

## Model Summary Rows

[
  {
    "model_id": "medsam_vit_b",
    "cathaction_sample_mean_dice": 0.08171376281972836,
    "cathaction_sample_mean_cldice": 0.05782871432914471,
    "cathaction_sample_min_dice": 0.00042762454564892024,
    "cathaction_sample_min_cldice": 0.0,
    "cathaction_prediction_nonempty_rate": 1.0,
    "cathaction_sample_mean_area_ratio": 9.189745959484494
  },
  {
    "model_id": "sam_vit_b",
    "cathaction_sample_mean_dice": 0.4306847770758381,
    "cathaction_sample_mean_cldice": 0.4664245104382771,
    "cathaction_sample_min_dice": 0.040098922451863625,
    "cathaction_sample_min_cldice": 0.023240241068263282,
    "cathaction_prediction_nonempty_rate": 1.0,
    "cathaction_sample_mean_area_ratio": 9.462109424317656
  },
  {
    "model_id": "sam_vit_l",
    "cathaction_sample_mean_dice": 0.32971383702509893,
    "cathaction_sample_mean_cldice": 0.32704955886426146,
    "cathaction_sample_min_dice": 0.048502986900393105,
    "cathaction_sample_min_cldice": 0.0,
    "cathaction_prediction_nonempty_rate": 1.0,
    "cathaction_sample_mean_area_ratio": 9.309671533223394
  }
]

## Ordering Boundary

{
  "ranked_model_count": 3,
  "synthetic_mean_stressor_dice_order": [
    "sam_vit_l",
    "sam_vit_b",
    "medsam_vit_b"
  ],
  "cathaction_sample_mean_dice_order": [
    "sam_vit_b",
    "sam_vit_l",
    "medsam_vit_b"
  ],
  "spearman_synthetic_mean_stressor_dice_vs_cathaction_mean_dice": 0.5,
  "rank_correlation_status": "smoke_rank_diagnostic_no_ci_n3_small_cathaction_sample",
  "claim_boundary": "This is a small-sample CathAction segmentation smoke. It can guide whether to scale CathAction evaluation, but it is not a final construct-validity estimate and has no confidence interval."
}

## Cleanup

{
  "delete_requested": true,
  "zip_path": "tmp/cathaction_s3e/segmentation_human_train.zip",
  "exists_before_cleanup": true,
  "deleted": true,
  "exists_after_cleanup": false
}

## Caveats

- The sample is small and deterministic; it is a smoke measurement, not a powered CathAction estimate.
- Prompts are label-derived oracle boxes, not deployable prompts.
- Larger CathAction payloads were not downloaded.
