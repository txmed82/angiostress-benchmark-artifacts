# AngioStress: A Deterministic Synthetic Stress-Test Benchmark for Frozen Endovascular Perception Models

- Paper type: `full_empirical`
- Outline maturity: `mature`

## One-Sentence Paper Idea

- Central thesis: A deterministic synthetic DSA stress-test benchmark can be evaluated by whether controlled stressor severity predicts frozen-model failure ordering on real angiography; the current AngioStress evidence supports reproducible measurement with partial, not complete, synthetic-to-real rank agreement.
- What readers learn: Synthetic stress tests are most useful when treated as construct-validity instruments rather than clinical proxies: agreement and disagreement with real angiography both expose what the benchmark measures.

## Story Spine

- Problem: Endovascular perception benchmarks need stress tests that expose model failure modes without training or fine-tuning new models.
- Gap: Synthetic angiography can control failure factors, but its scientific value depends on whether synthetic severity has construct validity against real angiography behavior.
- Method: AngioStress defines deterministic DSA-like projections, labeled synthetic stressors, and a frozen-model evaluation harness that compares synthetic failure ordering with real-angiography analogs from DIAS and CathAction.
- Main result: The current frozen-panel evidence shows mixed rank transfer: DIAS full-split rankings are discordant with synthetic ordering, while CathAction human segmentation gives stable partial agreement with MedSAM weakest and SAM ViT-B/SAM ViT-L swapped.
- Scope limit: The paper supports benchmark construction and bounded construct-validity estimation, not clinical accuracy, sim-to-real transfer, or a final universal leaderboard.

## Positioning

- closest_neighbor: DSA segmentation datasets and model baselines such as DIAS, CathAction, and promptable SAM/MedSAM evaluations on angiography frames.
- novelty_boundary: The contribution is not a new model or training method; it is a deterministic stress-test benchmark and a construct-validity measurement protocol for frozen off-the-shelf perception models.
- why_not_prior_work: Not recorded
- not_claiming: AngioStress improves model performance., Synthetic DSA projections are clinically realistic replacements for real angiography., The current results establish final synthetic-to-real transfer., The frozen panel is a clinical deployment ranking., Negative or discordant correlations are failures to hide rather than core measurement findings.

## Core Claims

- `C1` AngioStress provides a reproducible deterministic DSA-like stress-test scaffold with pixel-level ground truth and a frozen-model evaluation harness.
- `C2` Synthetic stressor severity has bounded construct validity: it partially predicts model failure ordering on CathAction human segmentation but not consistently on DIAS under the current fixed protocol.
- `C3` Reporting disagreement is part of the benchmark value because it identifies which real angiography surfaces are not captured by the current synthetic stressors.

## From Facts To Interpretation

- `Observed fact -> interpretation` The renderer and frozen-model harness produce deterministic, pixel-level stress-test cells and finite model metrics, so the benchmark artifact itself is reproducible enough to support measurement studies.
- `Observed fact -> interpretation` DIAS full-split rankings are discordant with the synthetic ordering, so synthetic stressor severity alone is not a sufficient proxy for all real angiography model failures.
- `Observed fact -> interpretation` CathAction human-segmentation rankings show stable partial agreement: MedSAM remains weakest, but SAM ViT-B and SAM ViT-L swap relative to the synthetic order.

## Evidence Boundaries

- Observed facts: The baseline and renderer-first harness are durably recorded., The frozen SAM/MedSAM panel has recorded synthetic and DIAS/CathAction metrics., DIAS full labeled split shows rank discordance with synthetic ordering under the fixed protocol., CathAction 128-pair nonempty human segmentation subset shows stable partial agreement with synthetic ordering., Temporary CathAction local payloads were deleted after bounded runs.
- Allowed interpretations: AngioStress is currently an auditable benchmark and measurement scaffold., Synthetic stressor severity has partial and surface-dependent construct validity in the current frozen panel., Rank disagreements are informative failure-surface evidence, not merely failed experiments.
- Do not claim: clinical accuracy, sim-to-real transfer, model improvement, new backbone training or fine-tuning, final universal frozen-model leaderboard, population-level CathAction confidence interval from the fixed subset
- Evidence gaps: all six requested stressors are not yet scaled across all real analog surfaces, failure taxonomy tags are not yet detector-backed across the full panel, paper-facing figures and tables still need to be rendered, additional model families would be needed for a stronger leaderboard claim

## Method

- Paper name: AngioStress
- Intuition: A stress-test benchmark should vary interpretable acquisition and scene factors while holding the frozen model, prompting, and metrics fixed, so rank changes can be interpreted as model sensitivity rather than training noise.
- Step: Generate deterministic DSA-like synthetic projections with pixel-level vessel ground truth.
- Step: Apply labeled stressors with severity parameters to define controlled benchmark cells.
- Step: Evaluate frozen off-the-shelf perception models under one prompt/metric protocol on synthetic and real-analog surfaces.
- Step: Compare model failure ordering with rank correlations, fixed-sample stability checks, and failure examples.

## Evaluation

- Setting: Frozen off-the-shelf endovascular perception evaluation under controlled synthetic stressors and real angiography analog surfaces.
- datasets_or_benchmarks: TopCoW-derived deterministic synthetic DSA-like projections, DIAS labeled DSA test sequences, CathAction human segmentation image-mask pairs
- baselines: SAM ViT-B, SAM ViT-L, MedSAM ViT-B, accepted TopCoW ResEncM renderer sanity baseline
- metrics: Dice, clDice, rank ordering, Spearman rank correlation, Kendall rank correlation where available, bootstrap rank-stability diagnostics, prediction nonempty rate, failure taxonomy tags when available
- controlled_factors: stressor type and severity, fixed frozen model weights, fixed prompt protocol, fixed metric implementation, deterministic sampling for bounded subsets

## Analysis Plan

- `A1` Synthetic stressor degradation curves (dose-response / benchmark sanity)
- `A2` DIAS full-test split rank correlation (real-data construct-validity check)
- `A3` CathAction human-segmentation subset rank stability (real-data construct-validity check)
- `A4` Cross-surface rank synthesis (construct-validity synthesis)
- `A5` Representative failure and overlay audit (failure taxonomy / qualitative validation)
- `A6` Sampling and mask-boundary sensitivity (robustness / sensitivity)

## Reviewer Objections

- The synthetic benchmark may not be realistic enough to justify real-angiography claims. -> claim_downgrade
- The model panel is too small for a general leaderboard. -> limitation
- Promptable SAM/MedSAM masks may be driven by prompt boxes rather than vessel understanding. -> analysis
- CathAction subset confidence intervals are not population-level estimates. -> writing
