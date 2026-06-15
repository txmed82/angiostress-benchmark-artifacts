---
license: other
pretty_name: AngioStress Benchmark Artifacts
task_categories:
- image-segmentation
tags:
- angiography
- dsa
- benchmark
- reproducibility
- construct-validity
---

# AngioStress Benchmark Artifacts

This repository contains the redistributable artifact package for **AngioStress: A Deterministic Stress-Test Benchmark for Construct Validity in Frozen Endovascular Perception Models**.

Author: Colin Son, MD, Seldinger, Inc., San Antonio, TX. ORCID: https://orcid.org/0000-0002-1782-0537

Public mirrors:

- GitHub: https://github.com/txmed82/angiostress-benchmark-artifacts
- Hugging Face dataset: https://huggingface.co/datasets/txmedai/angiostress-benchmark-artifacts

## Contents

- `paper/submission/`: compiled manuscript PDF, generated LaTeX, and compile report.
- `paper/figures/` and `paper/tables/`: paper-facing figure/table assets and their source data where present.
- `paper/evidence_ledger.*`, `paper/claim_evidence_map.*`, and `paper/paper_experiment_matrix.*`: traceability surfaces linking claims to derived evidence.
- `baseline/metric_contract.json`: comparison-ready baseline metric contract used for paper-facing interpretation.
- `derived/experiments-main/`: small text/CSV/JSON/Markdown derived summaries only.
- `MANIFEST.json`: file sizes and SHA-256 hashes for this release folder.

## Non-redistributed assets

This package intentionally does **not** redistribute raw DIAS, CathAction, TopCoW source data, SAM/MedSAM checkpoints, local caches, generated raw arrays, or model weights. Those assets remain under their respective upstream licenses and access routes. See `DATA_SOURCES.md` for source locations.

Generated at: 2026-06-15T13:16:00.402569+00:00
Source commit: a6f24deca026468bb2dec2457ffc3930f2f01d97
