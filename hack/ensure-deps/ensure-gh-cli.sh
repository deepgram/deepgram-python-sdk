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
VERSION="2.48.0"

SUDO_CMD="sudo"
if [[ "${CI_BUILD}" == "true" ]]; then
  SUDO_CMD=""
fi

CMD="gh"
if [[ -z "$(command -v ${CMD})" ]]; then
echo "Attempting install of ${CMD}..."
case "${BUILD_OS}" in
  Linux)
    curl -LO https://github.com/cli/cli/releases/download/v${VERSION}/gh_${VERSION}_linux_amd64.tar.gz
    tar -xvf gh_${VERSION}_linux_amd64.tar.gz
    pushd "./gh_${VERSION}_linux_amd64/bin" || exit 1
    chmod +x ${CMD}
    ${SUDO_CMD} install ./${CMD} /usr/local/bin
    popd || exit 1
    rm -rf ./gh_${VERSION}_linux_amd64
    rm gh_${VERSION}_linux_amd64.tar.gz
    ;;
  Darwin)
    brew install gh
    ;;
esac
fi
