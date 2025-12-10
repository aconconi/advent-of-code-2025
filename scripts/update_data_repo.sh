#!/usr/bin/env bash
set -euo pipefail

cd ./data 

if git diff --quiet -- .; then
    exit 0
fi

git add .
git commit -m "data files"
git push
