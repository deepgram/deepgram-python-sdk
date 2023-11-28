# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

class DeepgramApiKeyError(Exception):
    """
    Base class for exceptions raised for a missing Deepgram API Key.

    Attributes:
        message (str): The error message describing the exception.
    """
    def __init__(self, message: str):
        super().__init__(message)
        self.name = "DeepgramApiKeyError"

class DeepgramModuleError(Exception):
    """
    Base class for exceptions raised for a missing Deepgram module.

    Attributes:
        message (str): The error message describing the exception.
    """
    def __init__(self, message: str):
        super().__init__(message)
        self.name = "DeepgramModuleError"
