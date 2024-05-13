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
VERSION="0.10.0"

SUDO_CMD="sudo"
if [[ "${_CI_BUILD}" == "true" ]]; then
  SUDO_CMD=""
fi

CMD="shellcheck"
if [[ -z "$(command -v ${CMD})" ]]; then
echo "Attempting install of ${CMD}..."
case "${BUILD_OS}" in
  Linux)
    curl -LO https://github.com/koalaman/shellcheck/releases/download/v${VERSION}/shellcheck-v${VERSION}.linux.x86_64.tar.xz
    tar -xvf shellcheck-v${VERSION}.linux.x86_64.tar.xz
    pushd "./shellcheck-v${VERSION}" || exit 1
    chmod +x ${CMD}
    ${SUDO_CMD} install ./${CMD} /usr/local/bin
    popd || exit 1
    rm -rf ./shellcheck-v${VERSION}
    rm shellcheck-v${VERSION}.linux.x86_64.tar.xz
    ;;
  Darwin)
    # case "${BUILD_ARCH}" in
    #   x86_64)
    #     brew install shellcheck
    #     ;;
    #   arm64)
    #     brew install shellcheck
    #     ;;
    # esac
    brew install shellcheck
    ;;
esac
fi
