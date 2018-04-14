#!/usr/bin/env bash 
set -euo pipefail
source scripts/check_exit.sh

if [[ ! -d sparkle ]]; then
    curl -L -o sparkle.tar.bz2 https://github.com/sparkle-project/Sparkle/releases/download/1.18.1/Sparkle-1.18.1.tar.bz2
    mkdir -p sparkle
    tar -C sparkle -xf sparkle.tar.bz2
    rm sparkle.tar.bz2
fi

docker-compose run test ./scripts/sign_and_upload.sh 'sparkle/Sparkle Test App.app'
