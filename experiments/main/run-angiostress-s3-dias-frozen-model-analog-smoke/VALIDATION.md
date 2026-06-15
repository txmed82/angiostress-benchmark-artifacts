# VALIDATION

## Checks

- outputs_exist: true
- finite_metric_check: `1.0`
- frame_count: `6.0`
- prediction_nonempty_rate: `1.0`
- all_frame_mean_dice: `0.211319`
- all_frame_mean_cldice: `0.234490`

## Analog Rows

[
  {
    "family": "frame_thinning",
    "severity": 0,
    "subset_label": "all_frames",
    "frame_indices": [
      0,
      1,
      2,
      3,
      4,
      5
    ],
    "retained_frame_count": 6,
    "mean_dice": 0.21131857528530187,
    "mean_cldice": 0.2344899136404658,
    "min_dice": 0.20569080958470795,
    "min_cldice": 0.20649020662110537,
    "dice_delta_vs_family_severity0": 0.0,
    "cldice_delta_vs_family_severity0": 0.0
  },
  {
    "family": "frame_thinning",
    "severity": 1,
    "subset_label": "stride_2_frames",
    "frame_indices": [
      0,
      2,
      4
    ],
    "retained_frame_count": 3,
    "mean_dice": 0.21066191460164238,
    "mean_cldice": 0.2337869249966218,
    "min_dice": 0.20569080958470795,
    "min_cldice": 0.20664480070702798,
    "dice_delta_vs_family_severity0": -0.0006566606836594935,
    "cldice_delta_vs_family_severity0": -0.0007029886438440214
  },
  {
    "family": "frame_thinning",
    "severity": 2,
    "subset_label": "stride_3_frames",
    "frame_indices": [
      0,
      3
    ],
    "retained_frame_count": 2,
    "mean_dice": 0.21072529170650897,
    "mean_cldice": 0.25560629273735125,
    "min_dice": 0.20884762975999335,
    "min_cldice": 0.25079614215148904,
    "dice_delta_vs_family_severity0": -0.0005932835787929025,
    "cldice_delta_vs_family_severity0": 0.021116379096885435
  },
  {
    "family": "contrast_phase",
    "severity": 0,
    "subset_label": "all_frames",
    "frame_indices": [
      0,
      1,
      2,
      3,
      4,
      5
    ],
    "retained_frame_count": 6,
    "mean_dice": 0.21131857528530187,
    "mean_cldice": 0.2344899136404658,
    "min_dice": 0.20569080958470795,
    "min_cldice": 0.20649020662110537,
    "dice_delta_vs_family_severity0": 0.0,
    "cldice_delta_vs_family_severity0": 0.0
  },
  {
    "family": "contrast_phase",
    "severity": 1,
    "subset_label": "early_late_edge_frames",
    "frame_indices": [
      0,
      1,
      4,
      5
    ],
    "retained_frame_count": 4,
    "mean_dice": 0.2124044221185197,
    "mean_cldice": 0.23046095218292045,
    "min_dice": 0.20640058390246446,
    "min_cldice": 0.20649020662110537,
    "dice_delta_vs_family_severity0": 0.0010858468332178295,
    "cldice_delta_vs_family_severity0": -0.00402896145754536
  },
  {
    "family": "contrast_phase",
    "severity": 2,
    "subset_label": "lowest_intensity_frame",
    "frame_indices": [
      5
    ],
    "retained_frame_count": 1,
    "mean_dice": 0.21692217035139516,
    "mean_cldice": 0.20649020662110537,
    "min_dice": 0.21692217035139516,
    "min_cldice": 0.20649020662110537,
    "dice_delta_vs_family_severity0": 0.0056035950660932865,
    "cldice_delta_vs_family_severity0": -0.027999707019360442
  }
]

## Caveats

- DIAS provides a sequence-level mask here, so per-frame phase summaries are approximate.
- The SAM box prompt is derived from the label and is suitable for a harness smoke, not a deployable model setting.
- Device-overlay analogs remain deferred because CathAction data are not locally loaded.
