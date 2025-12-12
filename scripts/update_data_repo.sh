#!/usr/bin/env bash
set -euo pipefail

# Resolve the symlink to the actual data directory
DATA_DIR=$(readlink -f ./data)

# cd into the actual data repo
cd "$DATA_DIR"

git add .
git commit -m "data files" || exit 0  # exit 0 if nothing to commit
git push
