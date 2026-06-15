# Validation Summary

## Commands

```bash
/Users/colin/DeepScientist/quests/010/tmp/angiostress-s1-venv/bin/python -m py_compile experiments/main/run-angiostress-s1-frozen-model-smoke/run_sam_smoke.py
/Users/colin/DeepScientist/quests/010/tmp/angiostress-s1-venv/bin/python experiments/main/run-angiostress-s1-frozen-model-smoke/run_sam_smoke.py --config experiments/main/run-angiostress-s1-frozen-model-smoke/config.json --out experiments/main/run-angiostress-s1-frozen-model-smoke/outputs
```

The first evaluator attempt failed before inference because `scikit-image` was missing in the isolated virtualenv. After installing that metric dependency, the rerun completed successfully.

## Checks

- Required output files: present
- Per-cell rows: 10
- Prediction `.npy` masks: 10
- Prediction `.png` masks: 10
- Numeric metrics: finite
- Visual clean prediction: vessel-like and nonblank
- Visual `device_overlay_severity_2` prediction: visibly degraded with fragmentation/artifact pattern

## Metrics

- `clean_dice`: 0.9810482128526452
- `clean_cldice`: 0.9990412272291467
- `mean_stressor_dice`: 0.892633475863582
- `mean_stressor_cldice`: 0.920166815700077
- `mean_stressor_dice_delta_vs_clean`: -0.08841473698906317
- `mean_stressor_cldice_delta_vs_clean`: -0.07887441152906965
- `min_stressor_dice`: 0.5602697899102219
- `min_stressor_cldice`: 0.6424506218998289

## Family Summary

- `frame_thinning`: mean Dice 0.9798286687761569, mean clDice 0.9990412272291467
- `contrast_phase`: mean Dice 0.976262604634217, mean clDice 0.9966890244683944
- `device_overlay`: mean Dice 0.7218091541803723, mean clDice 0.76477019540269

## Boundary

This validates the frozen-model harness path for one generic promptable model only. It does not validate construct validity against DIAS/CathAction.
