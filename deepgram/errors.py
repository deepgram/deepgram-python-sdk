# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

class DeepgramApiKeyError(Exception):
    """
    Exception raised when a Deepgram API Key is missing or invalid.

    Attributes:
        message (str): The error message describing the exception.
    """

    def __init__(self, message: str = "Deepgram API Key is missing or invalid."):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"{self.__class__.__name__}: {self.message}"
