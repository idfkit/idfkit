# Address inventory of the retired sites

Captured 2026-09-02, while both sites still published, because it is unrecoverable
afterwards (FR-086). This is the input to `scripts/check_redirects.py`: every address
listed here must resolve after the cutover to `developers.idfkit.com` (FR-056, SC-020).

| File | Source | Addresses | Site `lastmod` |
| ---- | ------ | --------- | -------------- |
| `py.idfkit.com.sitemap.xml` | `https://py.idfkit.com/sitemap.xml` | 89 | 2026-07-07 |
| `js.idfkit.com.sitemap.xml` | `https://js.idfkit.com/sitemap.xml` | 28 | 2026-08-28 |

These are the **published** trees, not the working trees. `py.idfkit.com` still serves the
structure that predates the Diataxis migration of FR-060, which is why the inventory is taken
from the live sitemap rather than generated from `mkdocs.yml`. A reader's bookmark points at
what was published, not at what is in the repository.

Do not regenerate these files. Regenerating after the cutover would capture the redirect-only
build and make the check vacuous.
