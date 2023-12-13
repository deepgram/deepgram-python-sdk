# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import httpx
import json

from ..options import DeepgramClientOptions
from .errors import DeepgramError, DeepgramApiError, DeepgramUnknownApiError


class AbstractSyncRestClient:
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
    """

    def __init__(self, config: DeepgramClientOptions):
        if config is None:
            raise DeepgramError("Config are required")

        self.config = config

    def get(self, url: str, options=None, timeout=None):
        return self._handle_request(
            "GET", url, params=options, headers=self.config.headers, timeout=timeout
        )

    def post(self, url: str, options=None, timeout=None,  **kwargs):
        return self._handle_request(
            "POST", url, params=options, headers=self.config.headers, timeout=timeout, **kwargs
        )

    def put(self, url: str, options=None, timeout=None, **kwargs):
        return self._handle_request(
            "PUT", url, params=options, headers=self.config.headers, timeout=timeout, **kwargs
        )

    def patch(self, url: str, options=None, timeout=None, **kwargs):
        return self._handle_request(
            "PATCH", url, params=options, headers=self.config.headers, timeout=timeout, **kwargs
        )

    def delete(self, url: str, timeout=None):
        return self._handle_request("DELETE", url, headers=self.config.headers, timeout=timeout)

    def _handle_request(self, method, url, timeout, **kwargs):
        if timeout is None:
            timeout = httpx.Timeout(10.0, connect=10.0)
        try:
            with httpx.Client(timeout=timeout) as client:
                response = client.request(method, url, **kwargs)
                response.raise_for_status()
                return response.text
        except httpx._exceptions.HTTPError as e:
            if isinstance(e, httpx.HTTPStatusError):
                status_code = e.response.status_code or 500
                try:
                    json_object = json.loads(e.response.text)
                    raise DeepgramApiError(
                        json_object.get("message"), status_code, json.dumps(json_object)
                    ) from e
                except json.decoder.JSONDecodeError:
                    raise DeepgramUnknownApiError(e.response.text, status_code) from e
                except ValueError as e:
                    raise DeepgramUnknownApiError(e.response.text, status_code) from e
            else:
                raise
        except Exception as e:
            raise
