from .source import PrerecordedSource

def is_buffer_source(provided_source: PrerecordedSource) -> bool:
    return "buffer" in provided_source

def is_readstream_source(provided_source: PrerecordedSource) -> bool:
    return "stream" in provided_source

def is_url_source(provided_source: PrerecordedSource) ->  bool:
    return "url" in provided_source
