#!/usr/bin/env bash
set -euo pipefail
. scripts/check_exit.sh

if [[ $# != 1 ]]; then
    cat "usage: $0 <path_to_dmg>"
    exit 1
fi

ROOT=$(pwd)
APP_PATH="${ROOT}/${1}"
APP_NAME="$(basename "${APP_PATH}")"

mkdir -p tmp && chmod 700 tmp && pushd tmp
if [[ ! -f dsa_priv.pem ]]; then
    $ROOT/sparkle/bin/generate_keys
fi
mkdir -p "${APP_PATH}/Contents/Resources"
cp ./dsa_pub.pem "${APP_PATH}/Contents/Resources/test_app_only_dsa_pub.pem"
popd

./scripts/update_info_plist.py \
    --set "SUFeedURL=http://localhost:9090/sparkle/test/stable/appcast.xml" \
    --set "SUEnableAutomaticChecks=YES" \
    --set "SUScheduledCheckInterval=10" \
    --set "SUAllowsAutomaticUpdates=YES" \
    --set "SUAutomaticallyUpdate=YES" \
    "${APP_PATH}/Contents/Info.plist"

zip -q -r "${APP_PATH}.zip" "${APP_PATH}"


export DSA_SIGNATURE="$($ROOT/sparkle/bin/sign_update "${APP_PATH}.zip" tmp/dsa_priv.pem)"

python $ROOT/scripts/upload.py "${APP_PATH}.zip"
