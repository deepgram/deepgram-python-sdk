# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from typing import Dict
import re

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

    def __init__(self, api_key: str = "", url: str = "", headers: Dict[str, str] = None, options: Dict[str, str] = None):
        self.api_key = api_key
        if headers is None:
            self.headers = {
                "Accept": "application/json",
                "Authorization": f"Token {self.api_key}"
            }
        else:
            self.headers.update({
                "Accept": "application/json",
                "Authorization": f"Token {self.api_key}"
            })
        if len(url) == 0:
            url = "api.deepgram.com"
        self.url = self._get_url(url)
        if options is None:
            options = dict()
        self.options = options

    def set_apikey(self, api_key: str):
        self.api_key = api_key
        self.headers.update({
            "Accept": "application/json",
            "Authorization": f"Token {self.api_key}"
        })

    def _get_url(self, url):
        if not re.match(r'^https?://', url, re.IGNORECASE):
            url = 'https://' + url
        return url.strip('/')