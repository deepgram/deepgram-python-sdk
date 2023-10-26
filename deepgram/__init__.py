from deepgram.deepgram_client import DeepgramClient
from .types.deepgram_client_options import DeepgramClientOptions


def create_client(api_key: str, config_options: DeepgramClientOptions = None) -> DeepgramClient:
    """
    Create a DeepgramClient instance with the provided API key and optional configuration options.

    This function initializes and returns a DeepgramClient instance, which can be used to interact with the Deepgram API. You can provide an API key for authentication and customize the client's configuration by passing a DeepgramClientOptions object.

    Args:
        api_key (str): The Deepgram API key used for authentication.
        config_options (DeepgramClientOptions, optional): An optional configuration object specifying client options. If not provided, the default settings will be used.

    Returns:
        DeepgramClient: An instance of the DeepgramClient class for making requests to the Deepgram API.

    Example usage:
        To create a DeepgramClient instance with a custom configuration:

        >>> api_key = "your_api_key"
        >>> custom_options = DeepgramClientOptions(global_options={"url": "custom_url", "headers": {"Custom-Header": "value"}})
        >>> client = create_client(api_key, config_options=custom_options)

    Example usage with default settings:

        >>> api_key = "your_api_key"
        >>> client = create_client(api_key)
    """
    return DeepgramClient(api_key, config_options)
