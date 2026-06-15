# Validation Summary

## Commands

```bash
python3 -m py_compile experiments/main/run-angiostress-s0s1-renderer-smoke/run_renderer_smoke.py
python3 experiments/main/run-angiostress-s0s1-renderer-smoke/run_renderer_smoke.py --config experiments/main/run-angiostress-s0s1-renderer-smoke/config.json --out experiments/main/run-angiostress-s0s1-renderer-smoke/outputs
python3 experiments/main/run-angiostress-s0s1-renderer-smoke/run_renderer_smoke.py --config experiments/main/run-angiostress-s0s1-renderer-smoke/config.json --out experiments/main/run-angiostress-s0s1-renderer-smoke/outputs_rerun_check
```

## Checks

- Required output files: present
- Manifest cell count: 9
- Cell `.npy` count: 9
- Numeric metrics: finite
- Fresh rerun output hashes: matched
- Fresh rerun per-cell hashes: matched
- Clean preview: nonblank
- Device overlay severity 2 preview: visible device stressor

## Metrics

- `angiostress_renderer_success`: 1.0
- `angiostress_renderer_cell_count`: 9.0
- `angiostress_renderer_family_count`: 3.0
- `angiostress_renderer_deterministic_hash_match`: 1.0
- `angiostress_renderer_projected_gt_area_pixels`: 8233.0
- `angiostress_renderer_projected_gt_area_fraction`: 0.1256256103515625
- `angiostress_renderer_projected_gt_components_2d`: 2.0
- `angiostress_renderer_clean_gt_self_dice`: 1.0
- `angiostress_renderer_clean_gt_self_cldice`: 1.0
- `angiostress_renderer_finite_metric_check`: 1.0
- `angiostress_renderer_frozen_model_smoke_completed`: 0.0

## Boundary

This validates renderer/stressor feasibility only. It does not validate synthetic-to-real construct validity and does not compare frozen 2D DSA model failure orderings.
