# Preservation and persistent identifiers

NiceTryGPT uses separate mechanisms for source preservation, versioned releases, and scholarly citation.

## GitHub releases

GitHub releases are the project's versioned distribution point. Research or evaluation work should cite the exact NiceTryGPT release or commit used rather than the moving `main` branch.

Current public release: **v0.4.0**.

## Software Heritage

Software Heritage preserves public source code independently of GitHub and can assign Software Heritage persistent identifiers (SWHIDs) to archived objects.

The repository includes `.github/workflows/archive.yml` and a dependency-free archival helper at `scripts/request_swh_archive.py`.

The independent archive workflow requests preservation from the official Software Heritage Save Code Now API when:

- the archival workflow/helper changes on `main`;
- a GitHub release event is observed; or
- the workflow is started manually.

The release workflow also makes a direct **best-effort** archival request immediately after it creates a new GitHub release. This avoids relying on a downstream `release: published` workflow event, which may not be emitted when the release itself is created with the repository `GITHUB_TOKEN`.

Archival remains non-blocking for release publication: a temporary Software Heritage outage is visible in the release job but does not invalidate an otherwise successful GitHub release.

The first Save Code Now request completed successfully on 2026-09-20 with a full visit. Its archived snapshot is:

- **SWHID:** `swh:1:snp:6c77799e7623abf2653ab9363d3e2f57899174cf`
- **Save request:** [#2485366](https://archive.softwareheritage.org/api/1/origin/save/2485366/)
- **Snapshot API:** [6c77799e7623abf2653ab9363d3e2f57899174cf](https://archive.softwareheritage.org/api/1/snapshot/6c77799e7623abf2653ab9363d3e2f57899174cf/)

This SWHID identifies the archived repository snapshot independently of GitHub. Future release-triggered archive visits can produce newer snapshots while this identifier remains stable for the preserved object.

## Zenodo and DOI

NiceTryGPT v0.2.0 is archived on Zenodo as record [22858477](https://zenodo.org/records/22858477) with version-specific DOI [`10.5281/zenodo.22858477`](https://doi.org/10.5281/zenodo.22858477).

The repository uses `CITATION.cff` as its canonical software citation metadata. A `.zenodo.json` file is deliberately not included because Zenodo gives it precedence over `CITATION.cff`, and the project does not currently need Zenodo-specific grant, community, or relationship metadata.

The maintainer's GitHub account and `aleff-github/NiceTryGPT` repository are connected to Zenodo. The v0.4.0 release metadata intentionally does not reuse the v0.2.0 DOI. Once Zenodo mints the v0.4.0 deposit, its version-specific DOI should be added to `CITATION.cff`, CodeMeta, the website, and citation guidance in one synchronization update.

The DOI above identifies the archived v0.2.0 release only.

## Search indexing

The public site exposes:

- a canonical URL;
- `robots.txt`;
- `sitemap.xml`;
- Schema.org `SoftwareSourceCode` metadata;
- FAQ structured data;
- Open Graph/Twitter metadata;
- `llms.txt` as a concise machine-readable project guide.

For Google Search Console, use the URL-prefix property for `https://aleff-github.github.io/NiceTryGPT/`, verify ownership using a supported method, submit `sitemap.xml`, and request indexing of the homepage. Search engines may still take time to crawl and index a newly published site.
