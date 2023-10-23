

class DeepgramError(Exception):
    """
    Base class for exceptions raised by the Deepgram API client.

    Attributes:
        message (str): The error message describing the exception.
    """
    def __init__(self, message: str):
        super().__init__(message)
        self.name = "DeepgramError"

class DeepgramApiError(DeepgramError):
    """
    Exception raised for known errors (in json response format) related to the Deepgram API.

    Attributes:
        message (str): The error message describing the exception.
        status (str): The HTTP status associated with the API error.
    """
    def __init__(self, message: str, status: str, original_error = None):
        super().__init__(message)
        self.name = "DeepgramApiError"
        self.status = status
        self.message = message
        self.original_error = original_error
        
    def __str__(self):
        return f"{self.name}: {self.message} (Status: {self.status}) \n Error: {self.original_error}"

class DeepgramUnknownApiError(DeepgramApiError):
    """
    Exception raised for unknown errors related to the Deepgram API.

    Inherits from DeepgramApiError and includes the same attributes.

    Attributes:
        message (str): The error message describing the exception.
        status (str): The HTTP status associated with the API error.
    """
    def __init__(self, message: str, status: str):
        super().__init__(message, status)
        self.name = "DeepgramUnknownApiError"

class DeepgramUnknownError(DeepgramError):
    """
    Exception raised for unknown errors not specific to the Deepgram API.

    Attributes:
        message (str): The error message describing the exception.
        original_error (Exception): The original error that triggered this exception.
    """
    def __init__(self, message: str, original_error):
        super().__init__(message)
        self.name = "DeepgramUnknownError"
        self.original_error = original_error
