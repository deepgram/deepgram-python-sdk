from ._constants import DEFAULT_ENDPOINT
from ._types import Options
from ._version import __version__
from typing import Any, Union, Optional, IO, Mapping, Tuple, List
import aiohttp, urllib.parse, json, re, platform
import websockets, websockets.client

Payload = Optional[Union[dict, str, bytes, IO]]

def _prepare_headers(options: Options, headers: Mapping[str, str] = {}) -> dict:
    return {**headers,
        'Authorization': (options.get('auth_method') or 'Token') + ' ' + options['api_key'],
        'User-Agent': f'deepgram/{__version__} python/{platform.python_version()}'
    }

def _normalize_payload(payload: Payload) -> Optional[Union[bytes, IO]]:
    if payload is None:
        return None
    if isinstance(payload, dict):
        return json.dumps(payload).encode('utf-8')
    if isinstance(payload, str):
        return payload.encode('utf-8')
    return payload

def _make_query_string(params: Mapping[str, Any] = {}) -> str:
    def elem_decomposer(key: str, value: Any) -> List[Tuple[str, str]]:
        if value in [None, ""]:
            return []
        if isinstance(value, list):
            return [elem_decomposer(key, item) for item in value] # break into multiple parameters
        if isinstance(value, bool):
            return [(key, str(value).lower())] # make sure False and True stay lowercased in accordance with DG convention
        return [(key, str(value))]

    unflattened = [elem_decomposer(k, v) for k, v in params.items()] # sublist for each original parameter
    flattened = [item for group in unflattened for item in group] # flatten
    return ('?' if flattened else '') + urllib.parse.urlencode(flattened)


async def _request(path: str, options: Options, method: str = 'GET', payload: Payload = None, headers: Optional[Mapping[str, str]] = {}) -> Optional[dict]:
    destination = options.get('api_url', DEFAULT_ENDPOINT) + path
    updated_headers = _prepare_headers(options, headers)
    try:
        async with aiohttp.request(method, destination, data=_normalize_payload(payload), headers=updated_headers, raise_for_status=True) as resp:
            content = await resp.text()
            body = json.loads(content)
            if body.get('error'):
                raise Exception(f'DG: {content}')
            return body
    except aiohttp.ClientResponseError as e:
        raise Exception(f'DG: {e}')
    except aiohttp.ClientError as e:
        raise e

async def _socket_connect(path: str, options: Options, headers: Optional[Mapping[str, str]] = {}) -> websockets.client.WebSocketClientProtocol:
    destination = re.sub(r'^http', 'ws', options.get('api_url', DEFAULT_ENDPOINT)) + path
    updated_headers = _prepare_headers(options, headers)
    try:
        return await websockets.connect(destination, extra_headers=updated_headers, ping_interval=5)
        # If we're streaming too much faster than realtime, connection might close without an aggressive ping interval
    except websockets.exceptions.InvalidHandshake as e:
        raise Exception(f'DG: {e}')