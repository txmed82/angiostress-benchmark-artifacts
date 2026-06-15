# Finalize Integrity Audit

Created: 2026-06-15T05:10:29Z

## Verdict

The paper line is finalize-ready as a conservative submission package, not quest-complete by itself. Coverage, language, outline, checklist, citation, compile, and file-inventory checks pass, while the scientific claim remains bounded: AngioStress is supported as a reproducible measurement scaffold with mixed/partial synthetic-to-real rank evidence, not as a clinical-accuracy system or final construct-validity benchmark.

## Validation Snapshot

- Package type: `submission_package`
- Manuscript ready: `True`
- Submission ready: `True`
- Analysis groups: `8/8` ready
- Experiment matrix rows: `8/8` ready
- Submission checklist: `ready` at `paper/review/submission_checklist.json`
- Compile OK: `True` with `5` nonfatal warnings
- Academic outline ready: `True`; analysis plan ready: `True`
- Language firewall OK: `True` with `0` warnings
- Citation audit: `10` cited keys, `10` bibliography entries, missing citations `[]`, unused bibliography entries `[]`

## Evidence Provenance

- The evidence ledger contains 8 completed items and the paper experiment matrix contains 8 completed main-text rows.
- S3b DIAS evidence is anchored by `artifacts/reports/report-fe9dabda.json`, `experiments/analysis/s3b-dias-full-test-split-ranking/`, `paper/figures/data/model_surface_dice.csv`, and `paper/tables/table1_rank_summary.md`.
- S3f CathAction evidence is anchored by `artifacts/reports/report-97c8091c.json`, `experiments/analysis/s3f-cathaction-human-segmentation-subset-ranking/`, `paper/figures/data/model_surface_dice.csv`, and `paper/tables/table1_rank_summary.md`.

## Claim-Scope Check

- Supported: deterministic scaffold and finite frozen-model measurements for the evaluated three-model panel.
- Supported negative/mixed: DIAS full test-split rank evidence is discordant with synthetic ordering (`Spearman=-0.5`, `Kendall=-0.3333`, bootstrap Spearman mean `-0.425`, CI `[-0.675, -0.125]`).
- Supported partial: CathAction fixed subset shows partial agreement (`Spearman=0.5`, bootstrap mean `0.5285`, interval `[0.5, 1.0]`) mainly because MedSAM ViT-B remains weakest while SAM ViT-B/SAM ViT-L swap order.
- Excluded or deferred: clinical accuracy, clinical outcomes, positive sim-to-real transfer, final leaderboard, complete six-stressor release, final construct-validity estimate, and trained/fine-tuned backbone claims.

## Package Inventory

- Required files present: `True`
- Detailed file hashes and sizes are in `paper/finalize/package_inventory.json`; the figure catalog path is `paper/figures/figure_catalog.json`.
- Final claim ledger is in `paper/finalize/final_claim_ledger.json` and `paper/finalize/final_claim_ledger.md`.

## Nonfatal Warnings And Caveats

- Tectonic produced 5 overfull hbox warnings. They are presentation warnings and do not block the submission package, but a later typography polish pass could reduce them.
- The artifact contract generator previously showed an embedded 6-row matrix after bundle submission. The authoritative files for this package are `paper/paper_experiment_matrix.json` and `paper/manuscript_coverage.json`, both showing 8/8 ready groups after repair.
- Quest completion still requires explicit user approval before `artifact.complete_quest(...)`; this audit only supports asking for that approval or archiving the finalize-ready package.

## Recommended Next Action

Record a final decision that the paper package is finalize-ready with conservative claims, refresh summary/status surfaces, render the Git graph, commit the finalize artifacts, update checkpoint memory, and then request explicit quest-completion approval from the user.
