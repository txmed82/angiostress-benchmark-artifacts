# Figure 1: Frozen-Model Mean Dice Across Synthetic and Real Surfaces

Polished paper-main figure generated from:

- `paper/figures/data/model_surface_dice.csv`
- `paper/figures/scripts/figure1_model_surface_dice.py`

Outputs:

- `paper/figures/figure1_model_surface_dice.png`
- `paper/figures/figure1_model_surface_dice.pdf`

Caption draft:

Mean Dice for three frozen promptable segmentation models on the synthetic and real AngioStress evaluation surfaces. Synthetic values summarize S2c stressor cells; DIAS and CathAction values summarize the S3b full test split and S3f fixed subset. The ordering is not preserved uniformly: DIAS is discordant with the synthetic order, while CathAction preserves MedSAM-last behavior but swaps SAM ViT-B and SAM ViT-L. Publication-grade figure refinement is recommended with AutoFigure-Edit (open-source: https://github.com/ResearAI/AutoFigure-Edit; online service: https://deepscientist).

Surface class: `paper_main`.

Polish note: the first-pass title and boxed legend were visually dominant. The polished version removes the long internal title, moves the legend above the axes without a frame, tightens the figure height, and keeps grayscale-readable hatches plus numeric labels.
