# Copyright 2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

# detect the build OS
ifeq ($(OS),Windows_NT)
	build_OS := Windows
	NUL = NUL
else
	build_OS := $(shell uname -s 2>/dev/null || echo Unknown)
	NUL = /dev/null
endif

.DEFAULT_GOAL:=help

##### GLOBAL
ROOT_DIR := $(shell git rev-parse --show-toplevel)

# Add tooling binaries here and in hack/tools/Makefile
TOOLS_BIN_DIR := $(shell mktemp -d)

help: #### Display help
	@echo ''
	@echo 'Syntax: make <target>'
	@awk 'BEGIN {FS = ":.*## "; printf "\nTargets:\n"} /^[a-zA-Z_-]+:.*?#### / { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
	@echo ''
##### GLOBAL

##### LINTING TARGETS
.PHONY: version
version: #### display version of components
	@echo 'ROOT_DIR: $(ROOT_DIR)'
	@echo 'GOOS: $(GOOS)'
	@echo 'GOARCH: $(GOARCH)'
	@echo 'go version: $(shell go version)'

.PHONY: check lint pylint format black blackformat lint_files lint_diff static mypy mdlint shellcheck actionlint yamllint ### Performs all of the checks, lint'ing, etc available
check: lint static mdlint shellcheck actionlint yamllint

.PHONY: ensure-deps
ensure-deps: #### Ensure that all required dependency utilities are downloaded or installed
	hack/ensure-deps/ensure-dependencies.sh

GO_MODULES=$(shell find . -path "*/go.mod" | xargs -I _ dirname _)

PYTHON_FILES=.
lint_files: PYTHON_FILES=deepgram/ examples/
lint_diff: PYTHON_FILES=$(shell git diff --name-only --diff-filter=d main | grep -E '\.py$$')

lint_files lint_diff: #### Performs Python formatting
	black --target-version py310 $(PYTHON_FILES)

black blackformat format: lint_files

pylint: lint_files #### Performs Python linting
	pylint --disable=W0622 --disable=W0404 --disable=W0611 --rcfile .pylintrc deepgram

lint: pylint #### Performs Golang programming lint

static_files: PYTHON_FILES=deepgram/
static mypy: #### Performs static analysis
	mypy --config-file mypy.ini --python-version 3.10 --exclude examples --exclude tests/edge_cases --exclude tests/expected_failures $(PYTHON_FILES)

mdlint: #### Performs Markdown lint
	# mdlint rules with common errors and possible fixes can be found here:
	# https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md
	hack/check/check-mdlint.sh

shellcheck: #### Performs bash/shell lint
	hack/check/check-shell.sh

yamllint: #### Performs yaml lint
	hack/check/check-yaml.sh

actionlint: #### Performs GitHub Actions lint
	actionlint
##### LINTING TARGETS
