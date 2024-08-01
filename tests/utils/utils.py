# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import os


def get_query_params(url: str) -> str:
    pos = url.find("?")
    if pos == -1:
        return ""
    return url[pos + 1 :]


def create_dirs(fullpath: str) -> None:
    basedir = os.path.dirname(fullpath)
    os.makedirs(basedir, mode=0o700, exist_ok=True)


def save_metadata_bytes(filename: str, data: bytes) -> None:
    save_metadata_string(filename, data.decode())


def save_metadata_string(filename: str, data: str) -> None:
    # create directory
    create_dirs(filename)

    # save metadata
    with open(filename, "w", encoding="utf-8") as data_file:
        data_file.write(data)


def read_metadata_string(filename: str) -> str:
    with open(filename, "r", encoding="utf-8") as data_file:
        return data_file.read()


def read_metadata_bytes(filename: str) -> bytes:
    with open(filename, "rb") as data_file:
        return data_file.read()


def string_match_failure(expected: str, actual: str) -> None:
    if len(expected) != len(actual):
        raise ValueError("string lengths don't match")

    found = -1
    for i in range(len(expected)):
        if expected[i] != actual[i]:
            found = i
            break

    # expected
    for i in range(len(expected)):
        if i == found:
            print(f"\033[0;31m {expected[i]}", end="")
        else:
            print(f"\033[0m {expected[i]}", end="")
    print()

    # actual
    for i in range(len(expected)):
        if i == found:
            print(f"\033[0;31m {actual[i]}", end="")
        else:
            print(f"\033[0m {actual[i]}", end="")
    print()

    if found != -1:
        raise ValueError(f"string mismatch at position {found}")
