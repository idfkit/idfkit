#!/usr/bin/env bash

set -euo pipefail

# The four weather-browser files are part of the library's distribution and part of a page. They
# reached the page by symlink while the site lived inside the library; they are copied out of the
# installed distribution now, because a symlink does not survive a repository boundary.
#
# This runs before mkdocs on EVERY build, including the portable one, which is the point: the
# portable build copies docs/ and mkdocs.yml into a scratch directory with no src/ beside them, so
# a symlink there resolved to nothing. A missing asset stops the build rather than publishing a
# page with a broken widget.
uv run python scripts/copy_shipped_assets.py

uv run mkdocs build "$@"
# The unified site's host (FR-051). py.idfkit.com and js.idfkit.com are served by
# separate redirect-only builds and no longer publish this site (FR-056).
printf 'developers.idfkit.com\n' > site/CNAME
