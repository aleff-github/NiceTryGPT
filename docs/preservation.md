# Preservation and persistent identifiers

NiceTryGPT uses separate mechanisms for source preservation, versioned releases, and scholarly citation.

## GitHub releases

GitHub releases are the project's versioned distribution point. Research or evaluation work should cite the exact NiceTryGPT release or commit used rather than the moving `main` branch.

Current public release: **v0.2.0**.

## Software Heritage

Software Heritage preserves public source code independently of GitHub and can assign Software Heritage persistent identifiers (SWHIDs) to archived objects.

The repository includes `.github/workflows/archive.yml`. It requests archival from the official Software Heritage Save Code Now API when:

- the archival workflow is first merged to `main`;
- a GitHub release is published; or
- the workflow is started manually.

The archival workflow is intentionally separate from tests and releases so a temporary third-party archive outage cannot block normal project development.

Once the archive visit succeeds, a stable SWHID can be recorded here and, if useful, in `CITATION.cff` or release documentation.

## Zenodo and DOI

NiceTryGPT v0.2.0 is archived on Zenodo as record [22858477](https://zenodo.org/records/22858477) with version-specific DOI [`10.5281/zenodo.22858477`](https://doi.org/10.5281/zenodo.22858477).

The repository uses `CITATION.cff` as its canonical software citation metadata. A `.zenodo.json` file is deliberately not included because Zenodo gives it precedence over `CITATION.cff`, and the project does not currently need Zenodo-specific grant, community, or relationship metadata.

For future releases, the maintainer's GitHub account and `aleff-github/NiceTryGPT` repository are already connected to Zenodo. New release metadata should keep `CITATION.cff`, CodeMeta, the website, and the Zenodo record consistent.

The DOI above identifies the archived v0.2.0 release.

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
