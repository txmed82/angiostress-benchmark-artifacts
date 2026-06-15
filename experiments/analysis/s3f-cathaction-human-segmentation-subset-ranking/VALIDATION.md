# Validation

## Checks

- outputs_exist: true
- finite_metric_check: `1.0`
- model_count: `3.0`
- sample_count_per_model: `128.0`
- total_prediction_count: `384.0`
- local_zip_exists_after_cleanup: `False`

## Model Summary Rows

[
  {
    "model_id": "medsam_vit_b",
    "cathaction_sample_mean_dice": 0.09972911041072442,
    "cathaction_sample_mean_cldice": 0.08705523735746254,
    "cathaction_sample_min_dice": 0.0,
    "cathaction_sample_min_cldice": 0.0,
    "cathaction_prediction_nonempty_rate": 1.0,
    "cathaction_sample_mean_area_ratio": 9.191451020643179
  },
  {
    "model_id": "sam_vit_b",
    "cathaction_sample_mean_dice": 0.3647474714065172,
    "cathaction_sample_mean_cldice": 0.4022584581698785,
    "cathaction_sample_min_dice": 0.02230642739686852,
    "cathaction_sample_min_cldice": 0.0,
    "cathaction_prediction_nonempty_rate": 1.0,
    "cathaction_sample_mean_area_ratio": 11.619459637988667
  },
  {
    "model_id": "sam_vit_l",
    "cathaction_sample_mean_dice": 0.3463619309851356,
    "cathaction_sample_mean_cldice": 0.364272198772832,
    "cathaction_sample_min_dice": 0.0017263703064307294,
    "cathaction_sample_min_cldice": 0.0,
    "cathaction_prediction_nonempty_rate": 1.0,
    "cathaction_sample_mean_area_ratio": 10.404598252112663
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
  "rank_correlation_status": "subset_rank_diagnostic_bootstrap_stability_no_final_ci_n3",
  "claim_boundary": "This is a bounded CathAction human-segmentation subset check. It tests whether the frozen-panel ordering is stable enough to justify paper-outline repair, but it is not the final DIAS + CathAction construct-validity estimate across all stressors."
}

## Bootstrap Stability

{
  "bootstrap_iterations": 1000,
  "bootstrap_seed": 20260615,
  "sampled_pair_count": 128,
  "full_cathaction_order": [
    "sam_vit_b",
    "sam_vit_l",
    "medsam_vit_b"
  ],
  "synthetic_order": [
    "sam_vit_l",
    "sam_vit_b",
    "medsam_vit_b"
  ],
  "bootstrap_order_match_full_rate": 0.943,
  "bootstrap_order_match_synthetic_rate": 0.057,
  "bootstrap_spearman_mean": 0.5285,
  "bootstrap_spearman_ci95_percentile": [
    0.5,
    1.0
  ],
  "boundary": "Bootstrap resamples the fixed CathAction subset only; it is a sample-stability diagnostic, not a population-level final CI."
}

## Cleanup

{
  "delete_requested": true,
  "zip_path": "tmp/cathaction_s3f/segmentation_human_train.zip",
  "exists_before_cleanup": true,
  "deleted": true,
  "exists_after_cleanup": false
}

## Caveats

- The sample is deterministic and still limited to the human-segmentation training archive; it is a subset stability diagnostic, not a final powered construct-validity estimate.
- Prompts are label-derived oracle boxes, not deployable prompts.
- Larger CathAction payloads were not downloaded.
