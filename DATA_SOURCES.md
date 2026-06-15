# Data Sources and Redistribution Boundary

The public AngioStress artifact package includes manuscript files, paper-facing figures/tables, derived metric summaries, evidence ledgers, and reproducibility manifests. It does not redistribute upstream datasets or model checkpoints.

## Upstream sources

- DIAS real DSA dataset and code: https://github.com/lseventeen/DIAS and https://doi.org/10.5281/zenodo.11396520
- CathAction real DSA dataset and code: https://github.com/airvlab/cathaction
- TopCoW source anatomy labels: official TopCoW challenge/data release routes cited in the manuscript.
- SAM and MedSAM checkpoints: public project/model releases cited in the manuscript.

## Redistributed in this package

- Manuscript source and compiled PDF.
- Paper-facing figure/table assets.
- Evidence ledger, claim-evidence map, paper experiment matrix, coverage/language validation reports, and release inventory.
- Small derived summaries sufficient to inspect the reported paper-level analyses.

## Not redistributed

- Raw DIAS, CathAction, or TopCoW data.
- SAM/MedSAM or other model weights.
- Local dataset caches, generated raw arrays, masks, volumes, or checkpoint directories.
