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

usage() {
  cat <<EOF
usage: ${0} [FLAGS]
  Lints the project's shell scripts using Docker.

FLAGS
  -h    prints this help screen
EOF
}

while getopts ':h' opt; do
  case "${opt}" in
  h)
    usage 1>&2; exit 1
    ;;
  \?)
    { echo "invalid option: -${OPTARG}"; usage; } 1>&2; exit 1
    ;;
  :)
    echo "option -${OPTARG} requires an argument" 1>&2; exit 1
    ;;
  esac
done

shellcheck --version
find . -path ./vendor -prune -o -name "*.*sh" -type f -print0 | xargs -0 shellcheck
