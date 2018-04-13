#!/usr/bin/env bash -euo pipefail
. scripts/check_exit.sh

#curl -L -o sparkle.tar.bz2 https://github.com/sparkle-project/Sparkle/releases/download/1.18.1/Sparkle-1.18.1.tar.bz2
mkdir -p sparkle
tar -C sparkle -xf sparkle.tar.bz2
#rm sparkle.tar.bz2

./scripts/test.sh 'sparkle/Sparkle Test App.app'
