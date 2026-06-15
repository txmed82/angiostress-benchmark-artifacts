# VALIDATION

## Checks

- outputs_exist: true
- finite_metric_check: `1.0`
- model_count: `3.0`
- synthetic_item_count_per_model: `10.0`
- dias_frame_count_per_model: `6.0`
- total_prediction_count: `48.0`
- ranked_model_count: `3.0`

## Model Summary Rows

[
  {
    "model_id": "medsam_vit_b",
    "synthetic_clean_dice": 0.25539705183071804,
    "synthetic_clean_cldice": 0.23318951733744522,
    "synthetic_mean_stressor_dice": 0.2683099580428599,
    "synthetic_mean_stressor_cldice": 0.2479049986269016,
    "synthetic_min_stressor_dice": 0.24476502943163175,
    "synthetic_min_stressor_cldice": 0.22381904563850719,
    "synthetic_mean_stressor_dice_delta_vs_clean": 0.01291290621214192,
    "dias_all_frame_mean_dice": 0.21390124855402506,
    "dias_all_frame_mean_cldice": 0.13894415326050708,
    "dias_min_frame_dice": 0.21088959233933494,
    "dias_min_frame_cldice": 0.10874538385588296,
    "dias_prediction_nonempty_rate": 1.0,
    "dias_frame_thinning_severity2_dice_delta_vs_severity0": 0.0014820189423495889,
    "dias_contrast_phase_severity2_dice_delta_vs_severity0": -0.0002503915183459937
  },
  {
    "model_id": "sam_vit_b",
    "synthetic_clean_dice": 0.9810482128526452,
    "synthetic_clean_cldice": 0.9990412272291467,
    "synthetic_mean_stressor_dice": 0.892633475863582,
    "synthetic_mean_stressor_cldice": 0.920166815700077,
    "synthetic_min_stressor_dice": 0.5602697899102219,
    "synthetic_min_stressor_cldice": 0.6424506218998289,
    "synthetic_mean_stressor_dice_delta_vs_clean": -0.08841473698906317,
    "dias_all_frame_mean_dice": 0.21131857528530187,
    "dias_all_frame_mean_cldice": 0.2344899136404658,
    "dias_min_frame_dice": 0.20569080958470795,
    "dias_min_frame_cldice": 0.20649020662110537,
    "dias_prediction_nonempty_rate": 1.0,
    "dias_frame_thinning_severity2_dice_delta_vs_severity0": -0.0005932835787929025,
    "dias_contrast_phase_severity2_dice_delta_vs_severity0": 0.0056035950660932865
  },
  {
    "model_id": "sam_vit_l",
    "synthetic_clean_dice": 0.9751922599851154,
    "synthetic_clean_cldice": 0.9980806142034548,
    "synthetic_mean_stressor_dice": 0.9621867353873088,
    "synthetic_mean_stressor_cldice": 0.9660556448745515,
    "synthetic_min_stressor_dice": 0.9174072757435715,
    "synthetic_min_stressor_cldice": 0.8492660041366089,
    "synthetic_mean_stressor_dice_delta_vs_clean": -0.013005524597806524,
    "dias_all_frame_mean_dice": 0.1791642796798271,
    "dias_all_frame_mean_cldice": 0.20054321584737142,
    "dias_min_frame_dice": 0.17340681703572633,
    "dias_min_frame_cldice": 0.18087662337536436,
    "dias_prediction_nonempty_rate": 1.0,
    "dias_frame_thinning_severity2_dice_delta_vs_severity0": 0.00010972982735327208,
    "dias_contrast_phase_severity2_dice_delta_vs_severity0": 0.010608571731564903
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
  "dias_all_frame_mean_dice_order": [
    "medsam_vit_b",
    "sam_vit_b",
    "sam_vit_l"
  ],
  "spearman_synthetic_mean_stressor_dice_vs_dias_mean_dice": -1.0,
  "rank_correlation_status": "smoke_rank_diagnostic_no_ci_n3_one_sequence",
  "claim_boundary": "Three-model ordering rows are a smoke diagnostic only and cannot support construct-validity claims or confidence intervals."
}

## Caveats

- DIAS `s40` has a sequence-level mask, so per-frame phase summaries remain approximate.
- Prompts are label-derived smoke-test oracle prompts, not deployable prompts.
- Three models can produce a smoke rank diagnostic, but not a stable construct-validity estimate or confidence interval.
