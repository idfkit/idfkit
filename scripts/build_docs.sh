#!/usr/bin/env bash

set -euo pipefail

uv run mkdocs build "$@"
printf 'py.idfkit.com\n' > site/CNAME
