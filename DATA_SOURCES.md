# Data Sources and Redistribution Boundary

The public AngioStress artifact package includes benchmark code/configuration, comparison contracts, measured experiment outputs, and compact derived summaries. It does not include manuscript source, generated LaTeX, compiled manuscript PDFs, paper review/comment files, upstream datasets, or third-party model checkpoints.

## Upstream sources

- DIAS real DSA dataset and code: https://github.com/lseventeen/DIAS and https://doi.org/10.5281/zenodo.11396520
- CathAction real DSA dataset and code: https://github.com/airvlab/cathaction
- TopCoW source anatomy labels: official TopCoW challenge/data release routes.
- SAM and MedSAM checkpoints: public project/model releases.

## Redistributed in this package

- AngioStress benchmark/evaluation code, configs, validation records, and recorded experiment outputs.
- Baseline metric contract and compact run-level summaries.
- Derived JSON/CSV/Markdown summaries sufficient to inspect the recorded benchmark behavior.
- Release manifest with SHA-256 hashes and file sizes.

## Not redistributed

- Manuscript source, generated LaTeX, compiled manuscript PDFs, paper review/comment files, or paper planning/prose surfaces.
- Raw DIAS, CathAction, or TopCoW data.
- SAM/MedSAM or other third-party model weights/checkpoints.
- Local dataset caches, generated raw arrays, masks, volumes, or checkpoint directories.
