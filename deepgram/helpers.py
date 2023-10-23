import json
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode
from .types.prerecorded_source import PrerecordedSource

def strip_trailing_slash(url):
    parsed_url = urlparse(url)
    path = parsed_url.path.rstrip('/')
    modified_url = parsed_url._replace(path=path)
    return urlunparse(modified_url)

url = "https://example.com/path/"
stripped_url = strip_trailing_slash(url)

def is_buffer_source(provided_source: PrerecordedSource) -> bool:
    return "buffer" in provided_source

def is_readstream_source(provided_source: PrerecordedSource) -> bool:
    return "stream" in provided_source

def is_url_source(provided_source: PrerecordedSource) ->  bool:
    return "url" in provided_source

def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError as e:
        return False
    return True

def append_query_params(url, params=""):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    
    for key, value in params.items():
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

def convert_to_websocket_url(base_url, endpoint):
    parsed_url = urlparse(base_url)
    domain = parsed_url.netloc
    if parsed_url.scheme == "https":
        websocket_scheme = "wss"
    else:
        websocket_scheme = "ws"
    websocket_url = urlunparse((websocket_scheme, domain, endpoint, "", "", ""))
    return websocket_url