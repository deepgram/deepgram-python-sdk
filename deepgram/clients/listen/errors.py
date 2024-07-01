# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT


class DeepgramError(Exception):
    """
    Exception raised for unknown errors related to the Deepgram API.

    Attributes:
        message (str): The error message describing the exception.
    """

    def __init__(self, message: str):
        super().__init__(message)
        self.name = "DeepgramError"
        self.message = message

    def __str__(self):
        return f"{self.name}: {self.message}"


class DeepgramTypeError(Exception):
    """
    Exception raised for unknown errors related to unknown Types for Transcription.

    Attributes:
        message (str): The error message describing the exception.
    """

    def __init__(self, message: str):
        super().__init__(message)
        self.name = "DeepgramTypeError"
        self.message = message

    def __str__(self):
        return f"{self.name}: {self.message}"


class DeepgramWebsocketError(Exception):
    """
    Exception raised for known errors related to Websocket library.

    Attributes:
        message (str): The error message describing the exception.
    """

    def __init__(self, message: str):
        super().__init__(message)
        self.name = "DeepgramWebsocketError"
        self.message = message

    def __str__(self):
        return f"{self.name}: {self.message}"
