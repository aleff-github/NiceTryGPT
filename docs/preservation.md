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

NiceTryGPT already contains `CITATION.cff`, which Zenodo supports for GitHub software releases. A `.zenodo.json` file is deliberately not included because Zenodo gives it precedence over `CITATION.cff`, and the project does not currently need Zenodo-specific grant, community, or relationship metadata.

To mint a DOI for a release:

1. connect the maintainer's GitHub account to Zenodo;
2. enable `aleff-github/NiceTryGPT` in the Zenodo GitHub integration;
3. archive the desired GitHub release;
4. verify the generated Zenodo record and DOI;
5. add the DOI back to the canonical citation metadata in a normal pull request.

Do not invent or pre-reserve a DOI in repository metadata.

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
