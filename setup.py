# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from setuptools import setup, find_packages
import os.path

with open("README.md", "r", encoding="utf-8") as fh:
    LONG_DESCRIPTION = fh.read()

DESCRIPTION = (
    "The official Python SDK for the Deepgram automated speech recognition platform."
)

setup(
    name="deepgram-sdk",
    author="Deepgram",
    author_email="devrel@deepgram.com",
    url="https://github.com/deepgram/deepgram-python-sdk",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "httpx",
        "websockets",
        "typing-extensions; python_version < '3.8.0'",
        "dataclasses-json",
        "dataclasses",
        "typing_extensions",
        "python-dotenv",
        "asyncio",
        "aiohttp",
    ],
    keywords=["deepgram", "deepgram speech-to-text"],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)
