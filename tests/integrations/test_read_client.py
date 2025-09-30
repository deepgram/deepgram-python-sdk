"""Integration tests for Read client implementations."""

import pytest
from unittest.mock import Mock, AsyncMock, patch
import httpx
import json

from deepgram import DeepgramClient, AsyncDeepgramClient
from deepgram.core.client_wrapper import SyncClientWrapper, AsyncClientWrapper
from deepgram.core.api_error import ApiError
from deepgram.core.request_options import RequestOptions
from deepgram.environment import DeepgramClientEnvironment

from deepgram.read.client import ReadClient, AsyncReadClient
from deepgram.read.v1.client import V1Client as ReadV1Client, AsyncV1Client as ReadAsyncV1Client
from deepgram.read.v1.text.client import TextClient, AsyncTextClient

# Import request and response types for mocking
from deepgram.requests.read_v1request_text import ReadV1RequestTextParams
from deepgram.requests.read_v1request_url import ReadV1RequestUrlParams
from deepgram.types.read_v1response import ReadV1Response
from deepgram.read.v1.text.types.text_analyze_request_callback_method import TextAnalyzeRequestCallbackMethod
from deepgram.read.v1.text.types.text_analyze_request_summarize import TextAnalyzeRequestSummarize
from deepgram.read.v1.text.types.text_analyze_request_custom_topic_mode import TextAnalyzeRequestCustomTopicMode
from deepgram.read.v1.text.types.text_analyze_request_custom_intent_mode import TextAnalyzeRequestCustomIntentMode


class TestReadClient:
    """Test cases for Read Client."""

    @pytest.fixture
    def sync_client_wrapper(self, mock_api_key):
        """Create a sync client wrapper for testing."""
        return SyncClientWrapper(
            environment=DeepgramClientEnvironment.PRODUCTION,
            api_key=mock_api_key,
            headers={},
            httpx_client=Mock(),
            timeout=60.0
        )

    @pytest.fixture
    def async_client_wrapper(self, mock_api_key):
        """Create an async client wrapper for testing."""
        return AsyncClientWrapper(
            environment=DeepgramClientEnvironment.PRODUCTION,
            api_key=mock_api_key,
            headers={},
            httpx_client=AsyncMock(),
            timeout=60.0
        )

    def test_read_client_initialization(self, sync_client_wrapper):
        """Test ReadClient initialization."""
        client = ReadClient(client_wrapper=sync_client_wrapper)
        
        assert client is not None
        assert client._client_wrapper is sync_client_wrapper
        assert client._v1 is None  # Lazy loaded

    def test_async_read_client_initialization(self, async_client_wrapper):
        """Test AsyncReadClient initialization."""
        client = AsyncReadClient(client_wrapper=async_client_wrapper)
        
        assert client is not None
        assert client._client_wrapper is async_client_wrapper
        assert client._v1 is None  # Lazy loaded

    def test_read_client_v1_property_lazy_loading(self, sync_client_wrapper):
        """Test ReadClient v1 property lazy loading."""
        client = ReadClient(client_wrapper=sync_client_wrapper)
        
        # Initially None
        assert client._v1 is None
        
        # Access triggers lazy loading
        v1_client = client.v1
        assert client._v1 is not None
        assert isinstance(v1_client, ReadV1Client)
        
        # Subsequent access returns same instance
        assert client.v1 is v1_client

    def test_async_read_client_v1_property_lazy_loading(self, async_client_wrapper):
        """Test AsyncReadClient v1 property lazy loading."""
        client = AsyncReadClient(client_wrapper=async_client_wrapper)
        
        # Initially None
        assert client._v1 is None
        
        # Access triggers lazy loading
        v1_client = client.v1
        assert client._v1 is not None
        assert isinstance(v1_client, ReadAsyncV1Client)
        
        # Subsequent access returns same instance
        assert client.v1 is v1_client

    def test_read_client_raw_response_access(self, sync_client_wrapper):
        """Test ReadClient raw response access."""
        client = ReadClient(client_wrapper=sync_client_wrapper)
        
        raw_client = client.with_raw_response
        assert raw_client is not None
        assert raw_client is client._raw_client

    def test_async_read_client_raw_response_access(self, async_client_wrapper):
        """Test AsyncReadClient raw response access."""
        client = AsyncReadClient(client_wrapper=async_client_wrapper)
        
        raw_client = client.with_raw_response
        assert raw_client is not None
        assert raw_client is client._raw_client

    def test_read_client_integration_with_main_client(self, mock_api_key):
        """Test ReadClient integration with main DeepgramClient."""
        client = DeepgramClient(api_key=mock_api_key)
        
        read_client = client.read
        assert read_client is not None
        assert isinstance(read_client, ReadClient)

    def test_async_read_client_integration_with_main_client(self, mock_api_key):
        """Test AsyncReadClient integration with main AsyncDeepgramClient."""
        client = AsyncDeepgramClient(api_key=mock_api_key)
        
        read_client = client.read
        assert read_client is not None
        assert isinstance(read_client, AsyncReadClient)


class TestReadV1Client:
    """Test cases for Read V1 Client."""

    @pytest.fixture
    def sync_client_wrapper(self, mock_api_key):
        """Create a sync client wrapper for testing."""
        return SyncClientWrapper(
            environment=DeepgramClientEnvironment.PRODUCTION,
            api_key=mock_api_key,
            headers={},
            httpx_client=Mock(),
            timeout=60.0
        )

    @pytest.fixture
    def async_client_wrapper(self, mock_api_key):
        """Create an async client wrapper for testing."""
        return AsyncClientWrapper(
            environment=DeepgramClientEnvironment.PRODUCTION,
            api_key=mock_api_key,
            headers={},
            httpx_client=AsyncMock(),
            timeout=60.0
        )

    def test_read_v1_client_initialization(self, sync_client_wrapper):
        """Test ReadV1Client initialization."""
        client = ReadV1Client(client_wrapper=sync_client_wrapper)
        
        assert client is not None
        assert client._client_wrapper is sync_client_wrapper
        assert client._text is None  # Lazy loaded

    def test_async_read_v1_client_initialization(self, async_client_wrapper):
        """Test AsyncReadV1Client initialization."""
        client = ReadAsyncV1Client(client_wrapper=async_client_wrapper)
        
        assert client is not None
        assert client._client_wrapper is async_client_wrapper
        assert client._text is None  # Lazy loaded

    def test_read_v1_client_text_property_lazy_loading(self, sync_client_wrapper):
        """Test ReadV1Client text property lazy loading."""
        client = ReadV1Client(client_wrapper=sync_client_wrapper)
        
        # Initially None
        assert client._text is None
        
        # Access triggers lazy loading
        text_client = client.text
        assert client._text is not None
        assert isinstance(text_client, TextClient)
        
        # Subsequent access returns same instance
        assert client.text is text_client

    def test_async_read_v1_client_text_property_lazy_loading(self, async_client_wrapper):
        """Test AsyncReadV1Client text property lazy loading."""
        client = ReadAsyncV1Client(client_wrapper=async_client_wrapper)
        
        # Initially None
        assert client._text is None
        
        # Access triggers lazy loading
        text_client = client.text
        assert client._text is not None
        assert isinstance(text_client, AsyncTextClient)
        
        # Subsequent access returns same instance
        assert client.text is text_client

    def test_read_v1_client_raw_response_access(self, sync_client_wrapper):
        """Test ReadV1Client raw response access."""
        client = ReadV1Client(client_wrapper=sync_client_wrapper)
        
        raw_client = client.with_raw_response
        assert raw_client is not None
        assert raw_client is client._raw_client

    def test_async_read_v1_client_raw_response_access(self, async_client_wrapper):
        """Test AsyncReadV1Client raw response access."""
        client = ReadAsyncV1Client(client_wrapper=async_client_wrapper)
        
        raw_client = client.with_raw_response
        assert raw_client is not None
        assert raw_client is client._raw_client


class TestTextClient:
    """Test cases for Text Client."""

    @pytest.fixture
    def sync_client_wrapper(self, mock_api_key):
        """Create a sync client wrapper for testing."""
        mock_httpx_client = Mock(spec=httpx.Client)
        return SyncClientWrapper(
            environment=DeepgramClientEnvironment.PRODUCTION,
            api_key=mock_api_key,
            headers={},
            httpx_client=mock_httpx_client,
            timeout=60.0
        )

    @pytest.fixture
    def async_client_wrapper(self, mock_api_key):
        """Create an async client wrapper for testing."""
        mock_httpx_client = AsyncMock(spec=httpx.AsyncClient)
        return AsyncClientWrapper(
            environment=DeepgramClientEnvironment.PRODUCTION,
            api_key=mock_api_key,
            headers={},
            httpx_client=mock_httpx_client,
            timeout=60.0
        )

    @pytest.fixture
    def mock_text_request_url(self):
        """Mock text analysis request with URL."""
        return ReadV1RequestUrlParams(url="https://example.com/article.html")

    @pytest.fixture
    def mock_text_request_text(self):
        """Mock text analysis request with direct text."""
        return ReadV1RequestTextParams(
            text="This is a sample text for analysis. It contains positive sentiment and discusses technology topics."
        )

    @pytest.fixture
    def mock_text_analysis_response(self):
        """Mock text analysis response data."""
        from deepgram.types.read_v1response_metadata import ReadV1ResponseMetadata
        from deepgram.types.read_v1response_results import ReadV1ResponseResults
        
        return ReadV1Response(
            metadata=ReadV1ResponseMetadata(),
            results=ReadV1ResponseResults()
        )

    def test_text_client_initialization(self, sync_client_wrapper):
        """Test TextClient initialization."""
        client = TextClient(client_wrapper=sync_client_wrapper)
        
        assert client is not None
        assert client._raw_client is not None

    def test_async_text_client_initialization(self, async_client_wrapper):
        """Test AsyncTextClient initialization."""
        client = AsyncTextClient(client_wrapper=async_client_wrapper)
        
        assert client is not None
        assert client._raw_client is not None

    def test_text_client_raw_response_access(self, sync_client_wrapper):
        """Test TextClient raw response access."""
        client = TextClient(client_wrapper=sync_client_wrapper)
        
        raw_client = client.with_raw_response
        assert raw_client is not None
        assert raw_client is client._raw_client

    def test_async_text_client_raw_response_access(self, async_client_wrapper):
        """Test AsyncTextClient raw response access."""
        client = AsyncTextClient(client_wrapper=async_client_wrapper)
        
        raw_client = client.with_raw_response
        assert raw_client is not None
        assert raw_client is client._raw_client

    @patch('deepgram.read.v1.text.raw_client.RawTextClient.analyze')
    def test_text_client_analyze_url(self, mock_analyze, sync_client_wrapper, mock_text_request_url, mock_text_analysis_response):
        """Test TextClient analyze method with URL."""
        # Mock the raw client response
        mock_response = Mock()
        mock_response.data = mock_text_analysis_response
        mock_analyze.return_value = mock_response
        
        client = TextClient(client_wrapper=sync_client_wrapper)
        
        result = client.analyze(request=mock_text_request_url)
        
        assert result is not None
        assert isinstance(result, ReadV1Response)
        assert result.metadata is not None
        
        # Verify raw client was called with correct parameters
        mock_analyze.assert_called_once_with(
            request=mock_text_request_url,
            callback=None,
            callback_method=None,
            sentiment=None,
            summarize=None,
            topics=None,
            custom_topic=None,
            custom_topic_mode=None,
            intents=None,
            custom_intent=None,
            custom_intent_mode=None,
            language=None,
            request_options=None
        )

    @patch('deepgram.read.v1.text.raw_client.RawTextClient.analyze')
    def test_text_client_analyze_text_with_all_features(self, mock_analyze, sync_client_wrapper, mock_text_request_text, mock_text_analysis_response):
        """Test TextClient analyze method with text and all features enabled."""
        # Mock the raw client response
        mock_response = Mock()
        mock_response.data = mock_text_analysis_response
        mock_analyze.return_value = mock_response
        
        client = TextClient(client_wrapper=sync_client_wrapper)
        
        result = client.analyze(
            request=mock_text_request_text,
            sentiment=True,
            summarize=True,
            topics=True,
            custom_topic=["technology", "AI"],
            custom_topic_mode="extended",
            intents=True,
            custom_intent=["inform", "explain"],
            custom_intent_mode="strict",
            language="en"
        )
        
        assert result is not None
        assert isinstance(result, ReadV1Response)
        
        # Verify raw client was called with all parameters
        mock_analyze.assert_called_once_with(
            request=mock_text_request_text,
            callback=None,
            callback_method=None,
            sentiment=True,
            summarize=True,
            topics=True,
            custom_topic=["technology", "AI"],
            custom_topic_mode="extended",
            intents=True,
            custom_intent=["inform", "explain"],
            custom_intent_mode="strict",
            language="en",
            request_options=None
        )

    @patch('deepgram.read.v1.text.raw_client.RawTextClient.analyze')
    def test_text_client_analyze_with_callback(self, mock_analyze, sync_client_wrapper, mock_text_request_url, mock_text_analysis_response):
        """Test TextClient analyze method with callback configuration."""
        # Mock the raw client response
        mock_response = Mock()
        mock_response.data = mock_text_analysis_response
        mock_analyze.return_value = mock_response
        
        client = TextClient(client_wrapper=sync_client_wrapper)
        
        callback_url = "https://example.com/callback"
        result = client.analyze(
            request=mock_text_request_url,
            callback=callback_url,
            callback_method="POST",
            sentiment=True
        )
        
        assert result is not None
        assert isinstance(result, ReadV1Response)
        
        # Verify raw client was called with callback parameters
        mock_analyze.assert_called_once_with(
            request=mock_text_request_url,
            callback=callback_url,
            callback_method="POST",
            sentiment=True,
            summarize=None,
            topics=None,
            custom_topic=None,
            custom_topic_mode=None,
            intents=None,
            custom_intent=None,
            custom_intent_mode=None,
            language=None,
            request_options=None
        )

    @patch('deepgram.read.v1.text.raw_client.RawTextClient.analyze')
    def test_text_client_analyze_with_request_options(self, mock_analyze, sync_client_wrapper, mock_text_request_text, mock_text_analysis_response):
        """Test TextClient analyze method with request options."""
        # Mock the raw client response
        mock_response = Mock()
        mock_response.data = mock_text_analysis_response
        mock_analyze.return_value = mock_response
        
        client = TextClient(client_wrapper=sync_client_wrapper)
        
        request_options = RequestOptions(
            additional_headers={"X-Custom-Header": "test-value"}
        )
        result = client.analyze(
            request=mock_text_request_text,
            topics=True,
            request_options=request_options
        )
        
        assert result is not None
        assert isinstance(result, ReadV1Response)
        
        # Verify raw client was called with request options
        mock_analyze.assert_called_once_with(
            request=mock_text_request_text,
            callback=None,
            callback_method=None,
            sentiment=None,
            summarize=None,
            topics=True,
            custom_topic=None,
            custom_topic_mode=None,
            intents=None,
            custom_intent=None,
            custom_intent_mode=None,
            language=None,
            request_options=request_options
        )

    @patch('deepgram.read.v1.text.raw_client.AsyncRawTextClient.analyze')
    @pytest.mark.asyncio
    async def test_async_text_client_analyze_url(self, mock_analyze, async_client_wrapper, mock_text_request_url, mock_text_analysis_response):
        """Test AsyncTextClient analyze method with URL."""
        # Mock the async raw client response
        mock_response = Mock()
        mock_response.data = mock_text_analysis_response
        mock_analyze.return_value = mock_response
        
        client = AsyncTextClient(client_wrapper=async_client_wrapper)
        
        result = await client.analyze(request=mock_text_request_url)
        
        assert result is not None
        assert isinstance(result, ReadV1Response)
        assert result.metadata is not None
        
        # Verify async raw client was called with correct parameters
        mock_analyze.assert_called_once_with(
            request=mock_text_request_url,
            callback=None,
            callback_method=None,
            sentiment=None,
            summarize=None,
            topics=None,
            custom_topic=None,
            custom_topic_mode=None,
            intents=None,
            custom_intent=None,
            custom_intent_mode=None,
            language=None,
            request_options=None
        )

    @patch('deepgram.read.v1.text.raw_client.AsyncRawTextClient.analyze')
    @pytest.mark.asyncio
    async def test_async_text_client_analyze_with_all_features(self, mock_analyze, async_client_wrapper, mock_text_request_text, mock_text_analysis_response):
        """Test AsyncTextClient analyze method with all features enabled."""
        # Mock the async raw client response
        mock_response = Mock()
        mock_response.data = mock_text_analysis_response
        mock_analyze.return_value = mock_response
        
        client = AsyncTextClient(client_wrapper=async_client_wrapper)
        
        result = await client.analyze(
            request=mock_text_request_text,
            sentiment=True,
            summarize=True,
            topics=True,
            custom_topic="machine learning",
            custom_topic_mode="strict",
            intents=True,
            custom_intent=["question", "request"],
            custom_intent_mode="extended",
            language="en"
        )
        
        assert result is not None
        assert isinstance(result, ReadV1Response)
        
        # Verify async raw client was called with all parameters
        mock_analyze.assert_called_once_with(
            request=mock_text_request_text,
            callback=None,
            callback_method=None,
            sentiment=True,
            summarize=True,
            topics=True,
            custom_topic="machine learning",
            custom_topic_mode="strict",
            intents=True,
            custom_intent=["question", "request"],
            custom_intent_mode="extended",
            language="en",
            request_options=None
        )


class TestReadIntegrationScenarios:
    """Test Read integration scenarios."""

    def test_complete_read_workflow_sync(self, mock_api_key):
        """Test complete Read workflow using sync client."""
        with patch('deepgram.read.v1.text.raw_client.RawTextClient.analyze') as mock_analyze:
            # Mock the response
            mock_response = Mock()
            mock_response.data = Mock(spec=ReadV1Response)
            mock_response.data.metadata = Mock()
            mock_response.data.results = Mock()
            mock_response.data.results.summary = {"text": "Test summary"}
            mock_response.data.results.sentiments = {
                "average": {"sentiment": "positive", "sentiment_score": 0.7}
            }
            # Set request_id for assertion
            mock_response.data.request_id = "req-sync-123"
            mock_analyze.return_value = mock_response
            
            # Initialize client
            client = DeepgramClient(api_key=mock_api_key)
            
            # Create request
            request = ReadV1RequestTextParams(text="This is a test text for sentiment analysis.")
            
            # Access nested read functionality
            result = client.read.v1.text.analyze(
                request=request,
                sentiment=True,
                summarize=True
            )
            
            assert result is not None
            assert isinstance(result, ReadV1Response)
            assert result.request_id == "req-sync-123"
            
            # Verify the call was made
            mock_analyze.assert_called_once()

    @pytest.mark.asyncio
    async def test_complete_read_workflow_async(self, mock_api_key):
        """Test complete Read workflow using async client."""
        with patch('deepgram.read.v1.text.raw_client.AsyncRawTextClient.analyze') as mock_analyze:
            # Mock the async response
            mock_response = Mock()
            mock_response.data = Mock(spec=ReadV1Response)
            mock_response.data.metadata = Mock()
            mock_response.data.results = Mock()
            mock_response.data.results.topics = {
                "segments": [
                    {
                        "topics": [{"topic": "technology", "confidence_score": 0.9}]
                    }
                ]
            }
            # Set request_id for assertion
            mock_response.data.request_id = "req-async-456"
            mock_analyze.return_value = mock_response
            
            # Initialize async client
            client = AsyncDeepgramClient(api_key=mock_api_key)
            
            # Create request
            request = ReadV1RequestUrlParams(url="https://example.com/tech-article.html")
            
            # Access nested read functionality
            result = await client.read.v1.text.analyze(
                request=request,
                topics=True,
                custom_topic=["AI", "machine learning"]
            )
            
            assert result is not None
            assert isinstance(result, ReadV1Response)
            assert result.request_id == "req-async-456"
            
            # Verify the call was made
            mock_analyze.assert_called_once()

    def test_read_client_property_isolation(self, mock_api_key):
        """Test that read clients are properly isolated between instances."""
        client1 = DeepgramClient(api_key=mock_api_key)
        client2 = DeepgramClient(api_key=mock_api_key)
        
        read1 = client1.read
        read2 = client2.read
        
        # Verify they are different instances
        assert read1 is not read2
        assert read1._client_wrapper is not read2._client_wrapper
        
        # Verify nested clients are also different
        text1 = read1.v1.text
        text2 = read2.v1.text
        
        assert text1 is not text2

    @pytest.mark.asyncio
    async def test_mixed_sync_async_read_clients(self, mock_api_key):
        """Test mixing sync and async read clients."""
        sync_client = DeepgramClient(api_key=mock_api_key)
        async_client = AsyncDeepgramClient(api_key=mock_api_key)
        
        sync_read = sync_client.read
        async_read = async_client.read
        
        # Verify they are different types
        assert type(sync_read) != type(async_read)
        assert isinstance(sync_read, ReadClient)
        assert isinstance(async_read, AsyncReadClient)
        
        # Verify nested clients are also different types
        sync_text = sync_read.v1.text
        async_text = async_read.v1.text
        
        assert type(sync_text) != type(async_text)
        assert isinstance(sync_text, TextClient)
        assert isinstance(async_text, AsyncTextClient)


class TestReadErrorHandling:
    """Test Read client error handling."""

    @pytest.fixture
    def sync_client_wrapper(self, mock_api_key):
        """Create a sync client wrapper for testing."""
        mock_httpx_client = Mock(spec=httpx.Client)
        return SyncClientWrapper(
            environment=DeepgramClientEnvironment.PRODUCTION,
            api_key=mock_api_key,
            headers={},
            httpx_client=mock_httpx_client,
            timeout=60.0
        )

    @pytest.fixture
    def async_client_wrapper(self, mock_api_key):
        """Create an async client wrapper for testing."""
        mock_httpx_client = AsyncMock(spec=httpx.AsyncClient)
        return AsyncClientWrapper(
            environment=DeepgramClientEnvironment.PRODUCTION,
            api_key=mock_api_key,
            headers={},
            httpx_client=mock_httpx_client,
            timeout=60.0
        )

    @patch('deepgram.read.v1.text.raw_client.RawTextClient.analyze')
    def test_text_client_api_error_handling(self, mock_analyze, sync_client_wrapper):
        """Test TextClient API error handling."""
        # Mock an API error
        mock_analyze.side_effect = ApiError(
            status_code=400,
            headers={},
            body="Invalid request parameters"
        )
        
        client = TextClient(client_wrapper=sync_client_wrapper)
        request = ReadV1RequestTextParams(text="Test text")
        
        with pytest.raises(ApiError) as exc_info:
            client.analyze(request=request)
        
        assert exc_info.value.status_code == 400
        assert "Invalid request parameters" in str(exc_info.value.body)

    @patch('deepgram.read.v1.text.raw_client.AsyncRawTextClient.analyze')
    @pytest.mark.asyncio
    async def test_async_text_client_api_error_handling(self, mock_analyze, async_client_wrapper):
        """Test AsyncTextClient API error handling."""
        # Mock an API error
        mock_analyze.side_effect = ApiError(
            status_code=429,
            headers={},
            body="Rate limit exceeded"
        )
        
        client = AsyncTextClient(client_wrapper=async_client_wrapper)
        request = ReadV1RequestUrlParams(url="https://example.com/article.html")
        
        with pytest.raises(ApiError) as exc_info:
            await client.analyze(request=request)
        
        assert exc_info.value.status_code == 429
        assert "Rate limit exceeded" in str(exc_info.value.body)

    @patch('deepgram.read.v1.text.raw_client.RawTextClient.analyze')
    def test_text_client_network_error_handling(self, mock_analyze, sync_client_wrapper):
        """Test TextClient network error handling."""
        # Mock a network error
        mock_analyze.side_effect = httpx.ConnectError("Connection failed")
        
        client = TextClient(client_wrapper=sync_client_wrapper)
        request = ReadV1RequestTextParams(text="Test text")
        
        with pytest.raises(httpx.ConnectError):
            client.analyze(request=request)

    @patch('deepgram.read.v1.text.raw_client.AsyncRawTextClient.analyze')
    @pytest.mark.asyncio
    async def test_async_text_client_network_error_handling(self, mock_analyze, async_client_wrapper):
        """Test AsyncTextClient network error handling."""
        # Mock a network error
        mock_analyze.side_effect = httpx.ConnectError("Async connection failed")
        
        client = AsyncTextClient(client_wrapper=async_client_wrapper)
        request = ReadV1RequestUrlParams(url="https://example.com/article.html")
        
        with pytest.raises(httpx.ConnectError):
            await client.analyze(request=request)

    def test_invalid_request_parameters(self, sync_client_wrapper):
        """Test handling of invalid request parameters."""
        client = TextClient(client_wrapper=sync_client_wrapper)
        
        # Test with invalid request (None)
        with pytest.raises((TypeError, AttributeError)):
            client.analyze(request=None)

    def test_client_wrapper_integration(self, sync_client_wrapper):
        """Test integration with client wrapper."""
        client = ReadClient(client_wrapper=sync_client_wrapper)
        
        # Test that client wrapper methods are accessible
        assert hasattr(client._client_wrapper, 'get_environment')
        assert hasattr(client._client_wrapper, 'get_headers')
        assert hasattr(client._client_wrapper, 'api_key')
        
        environment = client._client_wrapper.get_environment()
        headers = client._client_wrapper.get_headers()
        api_key = client._client_wrapper.api_key
        
        assert environment is not None
        assert isinstance(headers, dict)
        assert api_key is not None
