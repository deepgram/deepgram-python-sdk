#!/usr/bin/env bash

# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

set -o nounset
set -o pipefail
set -o xtrace

CI_BUILD="${CI_BUILD:-""}"
BUILD_OS=$(uname 2>/dev/null || echo Unknown)
# BUILD_ARCH=$(uname -m 2>/dev/null || echo Unknown)
ACTIONLINT_VERSION="1.6.27"

SUDO_CMD="sudo"
if [[ "${CI_BUILD}" == "true" ]]; then
  SUDO_CMD=""
fi

CMD="actionlint"
if [[ -z "$(command -v ${CMD})" ]]; then
echo "Attempting install of ${CMD}..."
case "${BUILD_OS}" in
  Linux)
    curl -LO https://github.com/rhysd/actionlint/releases/download/v${ACTIONLINT_VERSION}/actionlint_${ACTIONLINT_VERSION}_linux_amd64.tar.gz
    mkdir actionlint_${ACTIONLINT_VERSION}_linux_amd64
    mv actionlint_${ACTIONLINT_VERSION}_linux_amd64.tar.gz ./actionlint_${ACTIONLINT_VERSION}_linux_amd64
    pushd "./actionlint_${ACTIONLINT_VERSION}_linux_amd64" || exit 1
    tar -xvf actionlint_${ACTIONLINT_VERSION}_linux_amd64.tar.gz
    chmod +x ${CMD}
    ${SUDO_CMD} install ./${CMD} /usr/local/bin
    popd || exit 1
    rm -rf ./actionlint_${ACTIONLINT_VERSION}_linux_amd64
    rm actionlint_${ACTIONLINT_VERSION}_linux_amd64.tar.gz
    ;;
  Darwin)
    brew install actionlint
    ;;
esac
fi
