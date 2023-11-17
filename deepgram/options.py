# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

class DeepgramClientOptions:

    """
    Represents options for configuring a Deepgram client.

    This class allows you to customize various options for interacting with the Deepgram API.

    Attributes:
        api_key (str): A Deepgram API key used for authentication.
        global_options (dict): A dictionary containing global configuration options.
            - headers (dict): Optional headers for initializing the client.
            - url (str): The URL used to interact with production, On-prem, and other Deepgram environments. Defaults to `api.deepgram.com`.
    """

    def __init__(self, api_key):
        self.api_key = api_key
        self.global_options = {
            "headers": {
                "Accept": "application/json",
                "Authorization": f"Token {self.api_key}"
            },
            "url": "api.deepgram.com"
        }