#!/usr/bin/env bash

# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

set -o nounset
set -o pipefail

CHECK_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
REPO_DIR="$(dirname "${CHECK_DIR}")/.."

docker run --rm -t cytopia/yamllint --version
CONTAINER_NAME="dg_yamllint_$RANDOM"
docker run --name ${CONTAINER_NAME} -t -v "${REPO_DIR}":/deepgram-go-sdk:ro cytopia/yamllint -s -c /deepgram-go-sdk/.yamllintconfig.yaml /deepgram-go-sdk
EXIT_CODE=$(docker inspect ${CONTAINER_NAME} --format='{{.State.ExitCode}}')
docker rm -f ${CONTAINER_NAME} &> /dev/null

if [[ ${EXIT_CODE} == "0" ]]; then
  echo "yamllint passed!"
else
  echo "yamllint exit code ${EXIT_CODE}: YAML linting failed!"
  echo "Please fix the listed yamllint errors and verify using 'make yamllint'"
  exit "${EXIT_CODE}"
fi
