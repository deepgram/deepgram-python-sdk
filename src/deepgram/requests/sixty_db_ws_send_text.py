# Client -> server send_text WS message.

import typing_extensions


class SixtyDbWsSendTextParams(typing_extensions.TypedDict):
    context_id: str
    text: str
    """
    1+ chars. Cumulative max 50,000 chars per context.
    """
