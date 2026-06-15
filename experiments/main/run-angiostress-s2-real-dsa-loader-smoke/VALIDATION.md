# Validation

## Checks Passed

- Public DIAS repository reachable and shallow-cloned.
- Public CathAction repository reachable and shallow-cloned.
- CathAction project website reachable and source-audited.
- DIAS Zenodo record reachable.
- `DIAS.zip` downloaded locally with size `292444663` bytes.
- DIAS archive md5 matched published md5 `780f32df6fb2a5de5d476f385cf2e83b`.
- DIAS archive inventory parsed: 882 PNG files and 13 directories.
- DIAS sequence inventory parsed: 60 sequences across training, validation, and test splits.
- Selected DIAS test sequence `s40` extracted with 6 frame PNGs and one sequence-level label PNG.
- Extracted frames and label exist on disk.
- Preview image rendered and inspected as nonblank with mask overlay aligned to the visible vessel tree.
- Manifest validation found no missing required evidence files and no missing frame files.

## Key Values

- Selected frame count: `6`
- Selected frame size: `800 x 800`
- Selected label nonzero pixels: `71224`
- Selected label bbox: `[0, 21, 773, 799]`
- Frame thinning analog status: `available_for_dias_sequence`
- Contrast phase analog status: `available_for_dias_sequence`
- Device overlay analog status: `not_available_from_dias_loader_alone`

## Remaining Boundary

CathAction is source-audited but not locally loaded in this run. The device-overlay real-data analog remains pending until CathAction data or another trustworthy real device-mask source is loaded.
