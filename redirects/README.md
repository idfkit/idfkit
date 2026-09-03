# Redirects from the retired documentation sites

`py.idfkit.com` and `js.idfkit.com` are retired. Both stop publishing and both redirect
permanently to `developers.idfkit.com`, and no address either site published may break
(FR-056, SC-020). This directory holds the one map that says where each address goes, and this
page holds the format, the cutover procedure, and the revert.

| File | What it is |
| ---- | ---------- |
| `path-map.json` | The map. One file, both hosts. |
| `../old-sitemaps/` | The address inventory captured while both sites still published (FR-086). |
| `../scripts/build_redirect_site.py` | Builds a host's redirect pages from the map. |
| `../scripts/check_redirects.py` | Checks the published result against the inventory. |

## The format

`path-map.json`, UTF-8, JSON with no schema dependency, readable by `json.load` in Python and
`JSON.parse` in Node without installing anything.

```json
{
  "map_version": 1,
  "unified_site": "https://developers.idfkit.com",
  "retired_hosts": {
    "py.idfkit.com": {
      "fallback": "/",
      "prefix_fallbacks": { "/api/": "/reference/" },
      "routes": { "/api/document/": "/api/document/" }
    }
  },
  "notes": [
    { "host": "py.idfkit.com", "path": "/idfkit-dev-guide/", "note": "why this one moved" }
  ]
}
```

- **`map_version`** is an integer. A reader that does not know the version stops rather than
  guessing. It is `1`.
- **`unified_site`** is the origin every target is resolved against, with no trailing slash.
- **`retired_hosts`** is keyed by bare hostname, no scheme.
- **`routes`** is the exact table: one entry for every address the host published, taken from
  the captured sitemap. Keys and values are absolute paths beginning with `/`, and directory
  paths end with `/`, which is how MkDocs publishes them.
- **`prefix_fallbacks`** catches addresses that are not in `routes`. Keys are path prefixes,
  values are the section landing page they fall back to.
- **`fallback`** catches what no prefix catches. It is `/`.
- **`notes`** is a flat list of records, each naming a host, a path, and prose. Notes carry
  caveats, not routing: nothing resolves through them. A note may name a path that is not a
  published address, to record a dependency.

### Resolution

Given an incoming path on a retired host, in order:

1. an exact match in `routes`;
2. otherwise the **longest** matching prefix in `prefix_fallbacks`;
3. otherwise `fallback`.

The result is always a path, so the answer is never a 404 (FR-056). The target is
`unified_site` + that path.

`build_redirect_site.py` implements steps 1 to 3 in Python for the pages it writes ahead of
time, and emits the same table into `404.html`, where the browser applies the same three steps
to whatever address it was actually given. The two implementations were checked against each
other on the same inputs.

### What the build writes

For each host: one `index.html` per entry in `routes`, carrying a `<link rel="canonical">` and
a `<meta http-equiv="refresh">` at the new address plus a visible sentence with the link; a
`404.html` carrying the table; a `CNAME`; and a `REDIRECTS_ONLY` sentinel file that
`archive-retired-site.yml` uses to refuse to archive a redirect build by mistake.

The build verifies itself: it fails if any address in `../old-sitemaps/<host>.sitemap.xml` has
no entry in `routes`.

```bash
uv run python scripts/build_redirect_site.py --host py.idfkit.com --out site
uv run python scripts/build_redirect_site.py --host js.idfkit.com --out site
```

## What moved, and what did not

`py.idfkit.com` mostly survives the merge unchanged: 88 of its 89 addresses keep their path on
the unified site. The exception is `/idfkit-dev-guide/`, which has no same-path successor; the
map routes it to `/agent-references/` and says why.

`js.idfkit.com` is the side that moves, since its pages fold into the Python repository's docs
tree. Five of its addresses are the generated TypeScript API reference, which the unified site
does not carry yet; they land on the reference section landing page and are marked
`PROVISIONAL` in `notes` until the phase that pins a TypeDoc artefact repoints them.

## The cutover

Order matters. Steps 1 and 2 are irreversible if done in the wrong order.

1. **Archive both last full builds.** Run `archive-retired-site` in `idfkit` and in
   `idfkit-js`, from the Actions tab, leaving the defaults. Each checks out `gh-pages`,
   verifies it is the real published site and not a redirect build, and uploads it.
   **Do this before any deploy touches either `gh-pages` branch.** Both deploys use
   `force_orphan`, which replaces the branch with a single new commit and leaves the old build
   in neither the branch nor its history.
2. **Publish the unified site.** `deploy-docs.yml` in `idfkit` publishes
   `developers.idfkit.com`, which releases the `py.idfkit.com` custom domain from that
   repository.
3. **Stand up the `py.idfkit.com` Pages repository.** A Pages site has exactly one custom
   domain, so `py.idfkit.com` cannot be served from the same `gh-pages` branch as
   `developers.idfkit.com`. Create `idfkit/py.idfkit.com`, add an SSH deploy key with write
   access, put its private half in `idfkit` as the secret `PY_IDFKIT_COM_DEPLOY_KEY`, and
   enable Pages on `gh-pages` with the custom domain `py.idfkit.com`. DNS does not change:
   the record already points at `idfkit.github.io`.
4. **Publish the redirects.** Run `deploy-py-redirects` in `idfkit` and `deploy-js-redirects`
   in `idfkit-js`. Both refuse to run unless step 1's artefact exists and has not expired.
5. **Check.** Run `scripts/check_redirects.py` against the captured inventory.

`js.idfkit.com` needs no new repository: `idfkit-js`'s own `gh-pages` keeps serving it, with
redirect content instead of the site.

## Reversibility

### What is retained, and for how long

The last full build of each retired site is uploaded as a named workflow artefact:

| Artefact | Repository | Retention |
| -------- | ---------- | --------- |
| `py.idfkit.com-last-full-build` | `idfkit` | **90 days** |
| `js.idfkit.com-last-full-build` | `idfkit-js` | **90 days** |

90 days is GitHub's maximum for a public repository (public repositories allow 1 to 90 days,
private ones 1 to 400), and both repositories are public, so this is the longest window
available. The number is set in `archive-retired-site.yml` as `RETENTION_DAYS`, not left to a
default, and both redirect workflows refuse to publish unless an unexpired artefact under the
matching name exists. Each artefact carries an `ARCHIVE-MANIFEST.txt` naming the host, the
commit, the date, and the window.

### Nothing was deleted

The cutover deleted nothing. `idfkit-js/docs/`, `idfkit-js/mkdocs.yml` and `idfkit-js/CNAME`
are untouched and still build the site; `docs.yml` still builds it on every push to `main` and
simply does not deploy it. On the Python side no source was removed either: the unified site is
the same `docs/` tree, published at a new host.

### Reverting

Within the window, reverting is flipping levers back. Each is a single named variable at the
top of a workflow file.

**`js.idfkit.com`**, two edits in `idfkit-js`, in one commit:

1. `.github/workflows/deploy-js-redirects.yml`: `JS_IDFKIT_COM_MODE: off`
2. `.github/workflows/docs.yml`: `JS_IDFKIT_COM_MODE: full-site`

Push to `main`. `docs.yml` builds and deploys the site to `gh-pages` as before, and
`js.idfkit.com` serves it again. Exactly one of the two workflows may publish to `gh-pages`, so
flip both together. No artefact download is needed: the sources are still there.

**`py.idfkit.com`**, one edit in `idfkit`:

1. `.github/workflows/deploy-py-redirects.yml`: `PY_IDFKIT_COM_MODE: off`

That stops the redirect build. What the host serves afterwards is a decision, because the
Python sources moved on: `docs/` now builds the unified site, not the pre-Diataxis tree that
`py.idfkit.com` last published. Two ways back, both configuration:

- **Serve the unified site at the old host.** In `deploy-docs.yml` set `cname` back to
  `py.idfkit.com` and remove the custom domain from `idfkit/py.idfkit.com`. Fastest, and the
  content is current.
- **Serve exactly what was published.** Download `py.idfkit.com-last-full-build` from the
  `archive-retired-site` run, unpack it, and push it to `gh-pages` of
  `idfkit/py.idfkit.com`. This is the only route that restores the pre-Diataxis tree
  byte for byte, and it is the one the 90 day window exists for.

### What becomes irreversible, and when

Ninety days after the `archive-retired-site` run, its artefact expires and GitHub deletes it.
From that moment:

- The **published tree of `py.idfkit.com`** no longer exists anywhere. Its `gh-pages` branch
  was replaced by `force_orphan` at the cutover, and the sources that produced it have since
  been reorganised, so it cannot be rebuilt. This is the real point of no return.
- The **published tree of `js.idfkit.com`** no longer exists either, but this is milder: the
  sources are untouched in `idfkit-js`, so a full site can still be built and served. What is
  lost is the exact bytes readers were served, not the ability to serve a site.

Everything else stays reversible for as long as the workflow files do, because the levers are
in the repository and the sources were never deleted.

Both redirect workflows are gated on the artefact existing and being unexpired, so the window
cannot lapse unnoticed between deciding to cut over and doing it.

## Open items

- The five generated TypeScript API reference addresses are provisional, marked in `notes`.
  Repoint them when the TypeDoc artefact is pinned onto the unified site.
