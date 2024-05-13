#!/usr/bin/env bash

# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

set -o nounset
set -o pipefail
set -o xtrace

_CI_BUILD="${_CI_BUILD:-""}"
BUILD_OS=$(uname 2>/dev/null || echo Unknown)
# BUILD_ARCH=$(uname -m 2>/dev/null || echo Unknown)
VERSION="1.7.1"

SUDO_CMD="sudo"
if [[ "${_CI_BUILD}" == "true" ]]; then
  SUDO_CMD=""
fi

CMD="jq"
if [[ -z "$(command -v ${CMD})" ]]; then
echo "Attempting install of ${CMD}..."
case "${BUILD_OS}" in
  Linux)
    curl -L "https://github.com/stedolan/jq/releases/download/jq-${VERSION}/jq-linux64" -o "jq"
    chmod +x jq
    ${SUDO_CMD} mv ${CMD} /usr/local/bin
    ;;
  Darwin)
    brew install jq
    ;;
esac
fi
