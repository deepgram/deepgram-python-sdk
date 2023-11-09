from enum import Enum

class LiveTranscriptionEvents(Enum):
    Open = "open"
    Close = "close"
    Transcript = "Results"
    Metadata = "Metadata"
    Error = "error"
    Warning = "warning"
