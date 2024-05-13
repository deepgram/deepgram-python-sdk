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
# VERSION="1.7.1"

SUDO_CMD="sudo"
if [[ "${_CI_BUILD}" == "true" ]]; then
  SUDO_CMD=""
fi

CMD="diff3"
if [[ -z "$(command -v ${CMD})" ]]; then
echo "Attempting install of ${CMD}..."
case "${BUILD_OS}" in
  Linux)
    if [[ -f "/etc/redhat-release" ]]; then
        ${SUDO_CMD} yum -y install diffutils
    elif [[ "$(grep Ubuntu /etc/os-release)" != "" ]]; then
        ${SUDO_CMD} apt-get -y install diffutils
    else
        echo "**** Please install diffutils before proceeding *****"
        exit 1
    fi
    ;;
  Darwin)
    brew install diffutils
    ;;
esac
fi
