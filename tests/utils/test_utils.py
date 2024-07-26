# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import pytest

from .utils import (
    get_query_params,
    create_dirs,
    save_metadata_bytes,
    save_metadata_string,
    read_metadata_string,
    read_metadata_bytes,
    string_match_failure,
)


def test_get_query_params():
    assert get_query_params("http://example.com/path?name=test") == "name=test"
    assert get_query_params("http://example.com/path") == ""


def test_create_dirs(tmp_path):
    test_dir = tmp_path / "test_dir"
    test_file = test_dir / "test_file.txt"
    create_dirs(test_file)
    assert test_dir.exists()


def test_save_and_read_metadata_string(tmp_path):
    test_file = tmp_path / "test_file.txt"
    test_data = "test_data"
    save_metadata_string(test_file, test_data)
    assert read_metadata_string(test_file) == test_data


def test_save_and_read_metadata_bytes(tmp_path):
    test_file = tmp_path / "test_file.txt"
    test_data = b"test_data"
    save_metadata_bytes(test_file, test_data)
    assert read_metadata_bytes(test_file) == test_data


def test_string_match_failure():
    expected = "expected"
    actual = "exzected"
    with pytest.raises(ValueError):
        string_match_failure(expected, actual)
