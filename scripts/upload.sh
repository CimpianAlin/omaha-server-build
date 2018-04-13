#!/usr/bin/env bash -euo pipefail
. scripts/check_exit.sh

if [[ $# != 1 ]]; then
    cat "usage: $0 <path_to_dmg>"
    exit 1
fi

DMG=$1

./scripts/upload.py "${DMG}"
