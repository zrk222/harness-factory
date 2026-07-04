# Zenodo Publication

Use Zenodo to archive HSF releases and mint a DOI that can be cited by
researchers, compliance teams, and technical reviewers.

## Prepared Metadata

The repository includes:

- `.zenodo.json` for Zenodo's GitHub release archiving metadata.
- `CITATION.cff` for GitHub's citation panel and citation-aware tooling.

Zenodo uses `.zenodo.json` first when both files are present.

## GitHub Integration Path

1. Sign in to [Zenodo](https://zenodo.org/) with GitHub.
2. Open [Zenodo GitHub settings](https://zenodo.org/account/settings/github/).
3. Click `Sync now`.
4. Find `zrk222/harness-factory` and toggle it on.
5. Publish a new GitHub release after the integration is enabled.

Zenodo archives public GitHub repositories when a new release is created and
issues a DOI for the archived software release.

## API Path

If you prefer direct API publication, create a Zenodo personal access token
with:

- `deposit:write`
- `deposit:actions`

Set it locally as `ZENODO_ACCESS_TOKEN`, then use the Zenodo deposit API to
create the record, upload the release archive, apply metadata, and publish.

Do not commit tokens to the repository.

This repository also includes a direct helper:

```bash
python scripts/publish_zenodo.py --publish
```

The helper reads `ZENODO_ACCESS_TOKEN`, builds a git archive from `HEAD`,
uploads it to Zenodo, applies `.zenodo.json`, publishes the record, and writes
`docs/zenodo-publication-receipt.json`.

## Current Release

Current GitHub release:

```text
https://github.com/zrk222/harness-factory/releases/tag/v0.2.0
```

Published Zenodo archive:

```text
https://zenodo.org/records/21188398
https://doi.org/10.5281/zenodo.21188398
```
