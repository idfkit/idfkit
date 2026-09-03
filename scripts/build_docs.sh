#!/usr/bin/env bash

set -euo pipefail

uv run mkdocs build "$@"
# The unified site's host (FR-051). py.idfkit.com and js.idfkit.com are served by
# separate redirect-only builds and no longer publish this site (FR-056).
printf 'developers.idfkit.com\n' > site/CNAME
