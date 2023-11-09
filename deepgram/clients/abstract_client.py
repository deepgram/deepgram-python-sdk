# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import httpx
import json
from typing import Dict, Any, Optional

from ..errors import DeepgramApiError, DeepgramUnknownApiError, DeepgramUnknownError

class AbstractRestfulClient:
    """
    An abstract base class for a RESTful HTTP client.

    This class provides common HTTP methods (GET, POST, PUT, PATCH, DELETE) for making asynchronous HTTP requests.
    It handles error responses and provides basic JSON parsing.

    Args:
        url (Dict[str, str]): The base URL for the RESTful API, including any path segments.
        headers (Optional[Dict[str, Any]]): Optional HTTP headers to include in requests.

    Attributes:
        url (Dict[str, str]): The base URL for the RESTful API.
        client (httpx.AsyncClient): An asynchronous HTTP client for making requests.
        headers (Optional[Dict[str, Any]]): Optional HTTP headers to include in requests.

    Exceptions:
        DeepgramApiError: Raised for known API errors.
        DeepgramUnknownApiError: Raised for unknown API errors.
        DeepgramUnknownError: Raised for unexpected errors not specific to the API.
    """

    def __init__(self, url: Dict[str, str], headers: Optional[Dict[str, Any]]):
        self.url = url
        self.client = httpx.AsyncClient()
        self.headers = headers

    async def get(self, url: str, options=None):
        headers = self.headers
        return await self._handle_request('GET', url, params=options, headers=headers)

    async def post(self, url: str, options=None, **kwargs):
        headers = self.headers
        return await self._handle_request('POST', url, params=options, headers=headers, **kwargs)

    async def put(self, url: str, options=None, **kwargs):
        headers = self.headers
        return await self._handle_request('PUT', url, params=options, headers=headers, **kwargs)

    async def patch(self, url: str, options=None, **kwargs):
        headers = self.headers
        return await self._handle_request('PATCH', url, params=options, headers=headers, **kwargs)

    async def delete(self, url: str):
        headers = self.headers
        return await self._handle_request('DELETE', url, headers=headers)

    async def _handle_request(self, method, url, **kwargs):
        try:
            with httpx.Client() as client:
                response = client.request(method, url, **kwargs)

                response.raise_for_status()
                return response.json()
        except httpx._exceptions.HTTPError as e:
            if isinstance(e, httpx.HTTPStatusError):
                status_code = e.response.status_code or 500
                if is_json(e.response.text):
                    json_object = json.loads(e.response.text)
                    raise DeepgramApiError(json_object.get(
                        'err_msg'), status_code, json.dumps(json_object)) from e
                else:
                    raise DeepgramUnknownApiError(
                        e.response.text, status_code) from e
            else:
                raise
        except Exception as e:
            raise DeepgramUnknownError(
                "An unknown error occurred during the request.", e) from e
