# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import json
import io
from typing import Dict, Optional, List, Union

import httpx

from .helpers import append_query_params
from ....options import DeepgramClientOptions
from .errors import DeepgramError, DeepgramApiError, DeepgramUnknownApiError


class AbstractSyncRestClient:
    """
    An abstract base class for a RESTful HTTP client.

    This class provides common HTTP methods (GET, POST, PUT, PATCH, DELETE) for making asynchronous HTTP requests.
    It handles error responses and provides basic JSON parsing.

    Args:
        url (Dict): The base URL for the RESTful API, including any path segments.
        headers (Optional[Dict[str, Any]]): Optional HTTP headers to include in requests.
        params (Optional[Dict[str, Any]]): Optional query parameters to include in requests.
        timeout (Optional[httpx.Timeout]): Optional timeout configuration for requests.

    Exceptions:
        DeepgramApiError: Raised for known API errors.
        DeepgramUnknownApiError: Raised for unknown API errors.
    """

    _config: DeepgramClientOptions

    def __init__(self, config: DeepgramClientOptions):
        if config is None:
            raise DeepgramError("Config are required")
        self._config = config

    # pylint: disable=too-many-positional-arguments

    def get(
        self,
        url: str,
        options: Optional[Dict] = None,
        addons: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        timeout: Optional[httpx.Timeout] = None,
        **kwargs,
    ) -> str:
        """
        Make a GET request to the specified URL.
        """
        return self._handle_request(
            "GET",
            url,
            params=options,
            addons=addons,
            headers=headers,
            timeout=timeout,
            **kwargs,
        )

    def post_raw(
        self,
        url: str,
        options: Optional[Dict] = None,
        addons: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        timeout: Optional[httpx.Timeout] = None,
        **kwargs,
    ) -> httpx.Response:
        """
        Make a POST request to the specified URL and return response in raw bytes.
        """
        return self._handle_request_raw(
            "POST",
            url,
            params=options,
            addons=addons,
            headers=headers,
            timeout=timeout,
            **kwargs,
        )

    def post_memory(
        self,
        url: str,
        file_result: List,
        options: Optional[Dict] = None,
        addons: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        timeout: Optional[httpx.Timeout] = None,
        **kwargs,
    ) -> Dict[str, Union[str, io.BytesIO]]:
        """
        Make a POST request to the specified URL and return response in memory.
        """
        return self._handle_request_memory(
            "POST",
            url,
            file_result=file_result,
            params=options,
            addons=addons,
            headers=headers,
            timeout=timeout,
            **kwargs,
        )

    def post(
        self,
        url: str,
        options: Optional[Dict] = None,
        addons: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        timeout: Optional[httpx.Timeout] = None,
        **kwargs,
    ) -> str:
        """
        Make a POST request to the specified URL.
        """
        return self._handle_request(
            "POST",
            url,
            params=options,
            addons=addons,
            headers=headers,
            timeout=timeout,
            **kwargs,
        )

    def put(
        self,
        url: str,
        options: Optional[Dict] = None,
        addons: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        timeout: Optional[httpx.Timeout] = None,
        **kwargs,
    ) -> str:
        """
        Make a PUT request to the specified URL.
        """
        return self._handle_request(
            "PUT",
            url,
            params=options,
            addons=addons,
            headers=headers,
            timeout=timeout,
            **kwargs,
        )

    def patch(
        self,
        url: str,
        options: Optional[Dict] = None,
        addons: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        timeout: Optional[httpx.Timeout] = None,
        **kwargs,
    ) -> str:
        """
        Make a PATCH request to the specified URL.
        """
        return self._handle_request(
            "PATCH",
            url,
            params=options,
            addons=addons,
            headers=headers,
            timeout=timeout,
            **kwargs,
        )

    def delete(
        self,
        url: str,
        options: Optional[Dict] = None,
        addons: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        timeout: Optional[httpx.Timeout] = None,
        **kwargs,
    ) -> str:
        """
        Make a DELETE request to the specified URL.
        """
        return self._handle_request(
            "DELETE",
            url,
            params=options,
            addons=addons,
            headers=headers,
            timeout=timeout,
            **kwargs,
        )

    # pylint: disable-msg=too-many-locals,too-many-branches
    def _handle_request(
        self,
        method: str,
        url: str,
        params: Optional[Dict] = None,
        addons: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        timeout: Optional[httpx.Timeout] = None,
        **kwargs,
    ) -> str:
        _url = url
        if params is not None:
            _url = append_query_params(_url, params)
        if addons is not None:
            _url = append_query_params(_url, addons)
        _headers = self._config.headers
        if headers is not None:
            _headers.update(headers)
        if timeout is None:
            timeout = httpx.Timeout(30.0, connect=10.0)

        try:
            transport = kwargs.get("transport")
            with httpx.Client(timeout=timeout, transport=transport) as client:
                if transport:
                    kwargs.pop("transport")
                response = client.request(method, _url, headers=_headers, **kwargs)
                response.raise_for_status()
                return response.text

        except httpx.HTTPError as e1:
            if isinstance(e1, httpx.HTTPStatusError):
                status_code = e1.response.status_code or 500
                try:
                    json_object = json.loads(e1.response.text)
                    raise DeepgramApiError(
                        json_object.get("err_msg"),
                        str(status_code),
                        json.dumps(json_object),
                    ) from e1
                except json.decoder.JSONDecodeError as e2:
                    raise DeepgramUnknownApiError(e2.msg, str(status_code)) from e2
                except ValueError as e2:
                    raise DeepgramUnknownApiError(str(e2), str(status_code)) from e2
            else:
                raise  # pylint: disable-msg=try-except-raise
        except Exception:  # pylint: disable-msg=try-except-raise
            raise

    # pylint: enable-msg=too-many-locals,too-many-branches

    # pylint: disable-msg=too-many-branches,too-many-locals
    def _handle_request_memory(
        self,
        method: str,
        url: str,
        file_result: List,
        params: Optional[Dict] = None,
        addons: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        timeout: Optional[httpx.Timeout] = None,
        **kwargs,
    ) -> Dict[str, Union[str, io.BytesIO]]:
        _url = url
        if params is not None:
            _url = append_query_params(_url, params)
        if addons is not None:
            _url = append_query_params(_url, addons)
        _headers = self._config.headers
        if headers is not None:
            _headers.update(headers)
        if timeout is None:
            timeout = httpx.Timeout(30.0, connect=10.0)

        try:
            transport = kwargs.get("transport")
            with httpx.Client(timeout=timeout, transport=transport) as client:
                if transport:
                    kwargs.pop("transport")
                response = client.request(method, _url, headers=_headers, **kwargs)
                response.raise_for_status()

                ret: Dict[str, Union[str, io.BytesIO]] = {}
                for item in file_result:
                    if item in response.headers:
                        ret[item] = response.headers[item]
                        continue
                    tmp_item = f"dg-{item}"
                    if tmp_item in response.headers:
                        ret[item] = response.headers[tmp_item]
                        continue
                    tmp_item = f"x-dg-{item}"
                    if tmp_item in response.headers:
                        ret[item] = response.headers[tmp_item]
                ret["stream"] = io.BytesIO(response.content)
                return ret

        except httpx.HTTPError as e1:
            if isinstance(e1, httpx.HTTPStatusError):
                status_code = e1.response.status_code or 500
                try:
                    json_object = json.loads(e1.response.text)
                    raise DeepgramApiError(
                        json_object.get("err_msg"),
                        str(status_code),
                        json.dumps(json_object),
                    ) from e1
                except json.decoder.JSONDecodeError as e2:
                    raise DeepgramUnknownApiError(e2.msg, str(status_code)) from e2
                except ValueError as e2:
                    raise DeepgramUnknownApiError(str(e2), str(status_code)) from e2
            else:
                raise  # pylint: disable-msg=try-except-raise
        except Exception:  # pylint: disable-msg=try-except-raise
            raise

    # pylint: disable-msg=too-many-branches,too-many-locals

    # pylint: disable-msg=too-many-branches,too-many-locals
    def _handle_request_raw(
        self,
        method: str,
        url: str,
        params: Optional[Dict] = None,
        addons: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        timeout: Optional[httpx.Timeout] = None,
        **kwargs,
    ) -> httpx.Response:
        _url = url
        if params is not None:
            _url = append_query_params(_url, params)
        if addons is not None:
            _url = append_query_params(_url, addons)
        _headers = self._config.headers
        if headers is not None:
            _headers.update(headers)
        if timeout is None:
            timeout = httpx.Timeout(30.0, connect=10.0)

        try:
            transport = kwargs.get("transport")
            client = httpx.Client(timeout=timeout, transport=transport)
            if transport:
                kwargs.pop("transport")
            req = client.build_request(method, _url, headers=_headers, **kwargs)
            return client.send(req, stream=True)

        except httpx.HTTPError as e1:
            if isinstance(e1, httpx.HTTPStatusError):
                status_code = e1.response.status_code or 500
                try:
                    json_object = json.loads(e1.response.text)
                    raise DeepgramApiError(
                        json_object.get("err_msg"),
                        str(status_code),
                        json.dumps(json_object),
                    ) from e1
                except json.decoder.JSONDecodeError as e2:
                    raise DeepgramUnknownApiError(e2.msg, str(status_code)) from e2
                except ValueError as e2:
                    raise DeepgramUnknownApiError(str(e2), str(status_code)) from e2
            else:
                raise  # pylint: disable-msg=try-except-raise
        except Exception:  # pylint: disable-msg=try-except-raise
            raise

    # pylint: enable-msg=too-many-branches,too-many-locals
    # pylint: enable=too-many-positional-arguments
