#!/usr/bin/env bash 
set -euo pipefail
source scripts/check_exit.sh

if [[ $# != 2 ]]; then
    cat "usage: $0 <path_to_dmg> <dsa private signing key>"
    exit 1
fi

APP_PATH="${1}"
KEY_PATH="${2}"
APP_NAME="$(basename "${APP_PATH}")"

tmp_path="tmp/${APP_NAME}"
cp -f "${APP_PATH}" $tmp_path
export DSA_SIGNATURE="$(openssl dgst -sha1 -binary < $tmp_path|openssl dgst -dss1 -sign $KEY_PATH|base64)"
docker-compose run test python ./scripts/upload.py "${tmp_path}"