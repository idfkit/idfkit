# Address inventory of the retired sites

Captured 2026-09-02, while both sites still published, because it is unrecoverable
afterwards (FR-086). This is the input to `scripts/check_redirects.py`: every address
listed here must resolve after the cutover to `developers.idfkit.com` (FR-056, SC-020).

| File | Source | Addresses | Site `lastmod` |
| ---- | ------ | --------- | -------------- |
| `py.idfkit.com.sitemap.xml` | `https://py.idfkit.com/sitemap.xml` | 89 | 2026-07-07 |
| `js.idfkit.com.sitemap.xml` | `https://js.idfkit.com/sitemap.xml` | 28 | 2026-08-28 |
| `developers.idfkit.com.txt` | `./scripts/build_docs.sh` in this repository | 126 | 2026-09-03 |

These are the **published** trees, not the working trees. `py.idfkit.com` still serves the
structure that predates the Diataxis migration of FR-060, which is why the inventory is taken
from the live sitemap rather than generated from `mkdocs.yml`. A reader's bookmark points at
what was published, not at what is in the repository.

Do not regenerate these files. Regenerating after the cutover would capture the redirect-only
build and make the check vacuous.

## `developers.idfkit.com.txt`

Captured 2026-09-03, immediately before feature 003 moved `docs/` out of this repository
(003-FR-006). Unlike the two sitemaps above it is taken from a **build**, not from a live
site, because `developers.idfkit.com` has never published: the cutover of feature 001 had
not run when the move happened.

That makes it the same kind of evidence for a different reason. The two retired hosts'
inventories are unrecoverable because those sites stopped publishing. This one is
unrecoverable because after the move this repository can no longer build the site at all,
and a list regenerated in `idfkit-developers` would compare that repository against itself
rather than against what stood here.

It is the input to 003-T037: every address in it must resolve against the new home, with a
tolerance of zero.

Do not regenerate this file either.

## `developers.idfkit.com.retired.txt`

The 17 addresses in the inventory above that the site deliberately stopped serving, in the
same feature that captured it. Replaying the inventory must subtract these before comparing,
and must find nothing else missing.

They were never published: `developers.idfkit.com` had no DNS record and `deploy-docs.yml`
had never run, so there is no bookmark to break and no redirect to write. The file exists so
that the difference between "retired on purpose" and "lost in a migration" is written down
rather than remembered, which is the same reason the inventories themselves exist.
