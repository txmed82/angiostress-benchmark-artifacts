# Verification Notes

## Checks Completed

- Verified the one-case manifest exists and contains one TopCoW case.
- Verified the manifest volume and mask paths resolve locally.
- Read NIfTI headers from the compressed files without loading full arrays.
- Computed SHA256 hashes for the volume, mask, GT sanity report, frozen ResEncM report, checkpoint, and checkpoint metadata.
- Verified source-paper identities through arXiv records:
  - DIAS: `2306.12153`
  - CathAction: `2408.13126`
  - TopCoW: `2312.17670`

## Evidence Logs

- Manifest and report summary: `.ds/bash_exec/bash-3287dc2f/terminal.log`
- NIfTI/header/report verification: `.ds/bash_exec/bash-ade2bc42/terminal.log`
- Checkpoint existence and hash verification: `.ds/bash_exec/bash-99c8e979/terminal.log`

## Verification Verdict

`trusted_with_caveats`

The local TopCoW one-case source and frozen 3D segmentation sanity comparator are trustworthy enough for S0/S1 implementation planning. They do not satisfy the later real-DSA frozen-model comparison requirement and should not be cited as construct-validity evidence.
