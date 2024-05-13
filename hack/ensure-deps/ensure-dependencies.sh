#!/usr/bin/env bash

# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

# set -o errexit
set -o nounset
set -o pipefail
set -o xtrace

BUILD_OS=$(uname 2>/dev/null || echo Unknown)
REPO_PATH="$(git rev-parse --show-toplevel)"

case "${BUILD_OS}" in
  Linux)
    ;;
  Darwin)
    ;;
  *)
    echo "${BUILD_OS} is unsupported"
    exit 1
    ;;
esac

i=0

# these are must have dependencies to just get going
if [[ -z "$(command -v go)" ]]; then
    echo "Missing go"
    ((i=i+1))
fi
if [[ -z "$(command -v docker)" ]]; then
    echo "Missing docker"
    ((i=i+1))
fi
# these are must have dependencies to just get going

if [[ $i -gt 0 ]]; then
    echo "Total missing: $i"
    echo "Please install these minimal dependencies in order to continue"
    exit 1
fi

"${REPO_PATH}/hack/ensure-deps/ensure-actionlint.sh"
"${REPO_PATH}/hack/ensure-deps/ensure-shellcheck.sh"
"${REPO_PATH}/hack/ensure-deps/ensure-diffutils.sh"
"${REPO_PATH}/hack/ensure-deps/ensure-gh-cli.sh"
"${REPO_PATH}/hack/ensure-deps/ensure-jq.sh"
"${REPO_PATH}/hack/ensure-deps/ensure-portaudio.sh"

echo "No missing dependencies!"
