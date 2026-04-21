#!/usr/bin/env bash
# Record all .tape files in this directory.
# Each tape runs in an isolated temp directory so commands like
# `idfkit tmy --download ./weather/` or `idfkit migrate` don't
# leave artifacts in the repo. The resulting GIF is copied back here.
set -euo pipefail

TAPE_DIR="$(cd "$(dirname "$0")" && pwd)"

for tape in "$TAPE_DIR"/*.tape; do
    name="$(basename "$tape")"
    gif="$(grep -m1 '^Output ' "$tape" | awk '{print $2}')"
    if [ -z "$gif" ]; then
        echo "Skipping $name (no Output directive found)"
        continue
    fi

    echo "Recording $name → $gif"
    tmpdir="$(mktemp -d)"
    cp "$tape" "$tmpdir/$name"

    # Stage fixtures alongside the tape (small IDF, Python samples, etc.)
    if [ -d "$TAPE_DIR/fixtures" ]; then
        cp -R "$TAPE_DIR/fixtures/." "$tmpdir/"
    fi

    echo "  tmpdir: $tmpdir"
    # Strip inherited prompt/venv vars so VHS's shell starts with a clean PS1.
    # (`uv sync` exports a zsh-formatted PS1 that bash renders as literal.)
    (cd "$tmpdir" && unset PS1 PROMPT VIRTUAL_ENV_PROMPT && vhs "$name")

    if [ -f "$tmpdir/$gif" ]; then
        cp "$tmpdir/$gif" "$TAPE_DIR/$gif"
        echo "  Saved $gif"
    else
        echo "  Warning: $gif not produced"
    fi

    rm -rf "$tmpdir"
done
