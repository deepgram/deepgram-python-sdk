# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import setuptools
import os.path

with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.md'), encoding="utf8") as file:
    long_description = file.read()

setuptools.setup(
    name='deepgram-sdk',
    description='The official Python SDK for the Deepgram automated speech recognition platform.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://github.com/deepgram/deepgram-python-sdk',
    author='Luca Todd',
    author_email='luca.todd@deepgram.com',
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
    keywords='deepgram speech-to-text',
    packages=setuptools.find_packages(),
    install_requires=[
        'httpx',
        'websockets',
        'typing-extensions; python_version < "3.8.0"',
        'dataclasses-json',
        'dataclasses',
        'typing_extensions',
        'python-dotenv',
        'asyncio',
        'aiohttp'
    ],
)
