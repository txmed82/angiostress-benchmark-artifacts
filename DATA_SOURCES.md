# Data Sources and Redistribution Boundary

This package provides the runnable AngioStress benchmark scaffold, configuration, generated benchmark outputs, compact metrics, and validation records. Full real-dataset reruns require the upstream data and checkpoints below.

## Upstream sources

- DIAS real DSA dataset and code: https://github.com/lseventeen/DIAS and https://doi.org/10.5281/zenodo.11396520
- CathAction real DSA dataset and code: https://github.com/airvlab/cathaction
- TopCoW source anatomy labels: official TopCoW challenge/data release routes.
- SAM and MedSAM checkpoints: public project/model releases.

## Redistributed in this package

- AngioStress renderer, frozen-model panel, DIAS diagnostic, and CathAction diagnostic scripts.
- Per-run configs, `RUN.md`, `VALIDATION.md`, manifests, and recorded outputs.
- Generated synthetic benchmark arrays/previews and model prediction masks from the benchmark runs.
- Baseline metric contract and compact run-level summaries.
- Release manifest with SHA-256 hashes and file sizes.

## Not redistributed

- Manuscript source, generated LaTeX, compiled manuscript PDFs, or paper review/comment files.
- Raw DIAS, CathAction, or TopCoW source data.
- SAM/MedSAM or other third-party model weights/checkpoints.
- Private local caches or credentials.
