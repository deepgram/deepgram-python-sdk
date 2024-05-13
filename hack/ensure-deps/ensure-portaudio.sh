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

CMD="portaudio"
if [[ -z "$(command -v ${CMD})" ]]; then
echo "Attempting install of ${CMD}..."
case "${BUILD_OS}" in
  Linux)
    if [[ -f "/etc/redhat-release" ]]; then
        ${SUDO_CMD} yum -y install portaudio19-dev
    elif [[ "$(grep Ubuntu /etc/os-release)" != "" ]]; then
        ${SUDO_CMD} apt-get -y install portaudio19-dev
    else
        echo "**** Please install portaudio before proceeding *****"
        exit 1
    fi
    ;;
  Darwin)
    brew install portaudio
    ;;
esac
fi
