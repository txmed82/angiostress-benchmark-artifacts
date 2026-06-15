# Frozen-Model Dependency Audit

## Result

The active Python environment does not currently contain a usable frozen 2D model stack.

## Checked Packages

- `torch`: missing
- `torchvision`: missing
- `transformers`: missing
- `segment_anything`: missing
- `medsam`: missing
- `nnunetv2`: missing
- `cv2`: missing

## Route Selection

The selected bounded setup attempt is a quest-local virtual environment with:

- PyTorch and torchvision
- Meta Segment Anything package
- Public SAM ViT-B checkpoint

SAM is not an endovascular model, but it is an acceptable promptable frozen 2D segmentation smoke path for testing the harness and per-cell metric plumbing. It will not be treated as a final DIAS/CathAction comparator.

## Guardrails

- No training or fine-tuning.
- Use projected GT only for prompt construction and metric evaluation in this smoke pass.
- Record setup failure as a dependency blocker if the local install or checkpoint download fails.
