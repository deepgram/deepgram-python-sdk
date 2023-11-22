# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

class DeepgramMicrophoneError(Exception):
    """
    Exception raised for known errors related to Microphone library.

    Attributes:
        message (str): The error message describing the exception.
        status (str): The HTTP status associated with the API error.
        original_error (str - json): The original error that was raised.
    """
    def __init__(self, message: str):
        super().__init__(message)
        self.name = "DeepgramMicrophoneError"
        self.message = message
        
    def __str__(self):
        return f"{self.name}: {self.message}"