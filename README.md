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

This repository contains redistributable benchmark assets for **AngioStress: A Deterministic Stress-Test Benchmark for Construct Validity in Frozen Endovascular Perception Models**.

Author: Colin Son, MD, Seldinger, Inc., San Antonio, TX. ORCID: https://orcid.org/0000-0002-1782-0537

Public mirrors:

- GitHub: https://github.com/txmed82/angiostress-benchmark-artifacts
- Hugging Face dataset: https://huggingface.co/datasets/txmedai/angiostress-benchmark-artifacts

## Contents

- `code/experiments-main/`: benchmark/evaluation scripts, configs, validation records, and measured experiment outputs used for the AngioStress runs.
- `code/baseline/angiostress-s0-topcow-resencm/`: comparison-ready baseline contract and local baseline support files.
- `derived/experiments-main/`: compact derived JSON/CSV/Markdown summaries for the recorded experiment runs.
- `baseline/metric_contract.json`: canonical comparison-ready baseline metric contract.
- `MANIFEST.json`: file sizes and SHA-256 hashes for payload files in this release folder; the manifest file itself is excluded from its own hash list.

## Deliberately Not Included

This public artifact package intentionally excludes manuscript source, generated LaTeX, compiled manuscript PDFs, paper review/comment files, and paper planning/prose surfaces. The LaTeX submission zip is delivered only through the requested private Telegram attachment path.

It also does not redistribute raw DIAS, CathAction, or TopCoW data, local caches, generated raw arrays, or third-party model weights/checkpoints. Those assets remain under their respective upstream licenses and access routes. See `DATA_SOURCES.md`.

Cleaned at: 2026-06-15T13:59:42.127516+00:00
Source commit: a0786a46b574ea7a1d1d60eb22ce079b835a7875
