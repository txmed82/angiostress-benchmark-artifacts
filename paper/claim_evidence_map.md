# Claim-Evidence Map

- paper line: `main-outline-run`
- selected outline: `outline-001`
- draft checkpoint: `paper/draft.md`
- coverage validation: `paper/manuscript_coverage.json`
- status: manuscript-ready draft checkpoint; not submission-ready

## Supported Claims

### C1. Deterministic benchmark scaffold

AngioStress currently has a reproducible deterministic scaffold for DSA-like synthetic projection, pixel-level labels, stressor configuration, and frozen-model evaluation.

Evidence:
- `paper/evidence_ledger.json`
- `paper/evidence_ledger.md`
- `paper/selected_outline.json`
- `paper/draft.md`

Boundary:
- This supports a benchmark artifact checkpoint, not clinical validity.

### C2. Frozen-model panel measurement

The checkpoint measures three frozen, off-the-shelf segmentation models across synthetic stressor summaries and two real-angiography surfaces.

Evidence:
- S2c synthetic means in `paper/figures/data/model_surface_dice.csv`
- S3b DIAS full-test means in `paper/figures/data/model_surface_dice.csv`
- S3f CathAction subset means in `paper/figures/data/model_surface_dice.csv`
- `paper/figures/figure1_model_surface_dice.png`
- `paper/figures/figure1_model_surface_dice.pdf`
- `paper/tables/table1_rank_summary.md`

Boundary:
- The panel is fixed and frozen; no model training, fine-tuning, pruning, or backbone modification is claimed.

### C3. Mixed construct-validity signal

Synthetic-to-real rank transfer is mixed at this checkpoint. DIAS is discordant with the synthetic ordering, while the CathAction subset shows partial agreement driven mainly by stable MedSAM-last behavior and a SAM ViT-B / SAM ViT-L swap.

Evidence:
- `artifacts/reports/report-fe9dabda.json`
- `artifacts/reports/report-97c8091c.json`
- `paper/tables/table1_rank_summary.md`
- `paper/figures/figure1_model_surface_dice.md`
- `paper/draft.md`

Key values:
- DIAS full split: 20 sequences, 115 frames/model, 345 predictions, Spearman -0.5, Kendall -0.3333, sequence-bootstrap Spearman mean -0.425 with 95% CI [-0.675, -0.125].
- CathAction fixed subset: 128 nonempty pairs/model, 384 predictions, Spearman 0.5, fixed-subset bootstrap Spearman mean 0.5285 with percentile interval [0.5, 1.0].

Boundary:
- This is a construct-validity estimate, not proof that synthetic stressor severity generally predicts real clinical performance.

### C4. Current non-claims

The draft does not support a final leaderboard, a clinical-accuracy claim, a sim-to-real transfer claim, or a complete six-stressor AngioStress v0.1 release.

Evidence:
- `paper/draft.md`
- `paper/manuscript_coverage.json`
- `paper/selected_outline.json`

Boundary:
- Submission readiness remains blocked by citation/reference audit, figure polish, compiled PDF, and submission checklist.

## Displays

- Figure 1: `paper/figures/figure1_model_surface_dice.png`
- Figure 1 source data: `paper/figures/data/model_surface_dice.csv`
- Figure 1 script: `paper/figures/scripts/figure1_model_surface_dice.py`
- Table 1: `paper/tables/table1_rank_summary.md`

## Next Review Questions

- Are all metric claims tied to exact reports or source data?
- Does the text overstate construct validity beyond the DIAS/CathAction checkpoint evidence?
- Are citations sufficient and real after reference audit?
- Does the first-pass figure need polish before a submission package?
