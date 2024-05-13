#!/bin/bash

# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

set -o errexit
set -o nounset
set -o pipefail

# Change directories to the parent directory of the one in which this
# script is located.
cd "$(dirname "${BASH_SOURCE[0]}")/../.."

# mdlint rules with common errors and possible fixes can be found here:
# https://github.com/igorshubovych/markdownlint-cli
docker run -v "$PWD":/workdir \
  ghcr.io/igorshubovych/markdownlint-cli:latest \
  -i LICENSE \
  "*.md"
