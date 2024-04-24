# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from urllib.parse import urlparse, urlunparse, parse_qs, urlencode
from typing import Dict
import re


# This function appends query parameters to a URL
def append_query_params(url: str, params: Dict):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    for key, value in params.items():
        if value is None:
            continue
        if isinstance(value, bool):
            value = str(value).lower()
        if isinstance(value, list):
            for item in value:
                query_params[key] = query_params.get(key, []) + [str(item)]
        else:
            query_params[key] = [str(value)]

    updated_query_string = urlencode(query_params, doseq=True)
    updated_url = parsed_url._replace(query=updated_query_string).geturl()
    return updated_url


# This function converts a URL to a WebSocket URL
def convert_to_websocket_url(base_url: str, endpoint: str):
    if re.match(r"^https?://", base_url, re.IGNORECASE):
        base_url = base_url.replace("https://", "").replace("http://", "")
    if not re.match(r"^wss?://", base_url, re.IGNORECASE):
        base_url = "wss://" + base_url
    parsed_url = urlparse(base_url)
    domain = parsed_url.netloc
    websocket_url = urlunparse((parsed_url.scheme, domain, endpoint, "", "", ""))
    return websocket_url
