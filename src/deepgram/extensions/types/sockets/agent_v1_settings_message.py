# Agent V1 Settings Message - protected from auto-generation

import typing

import pydantic
from ....core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel

# Cross-version constrained types
if IS_PYDANTIC_V2:
    IntContextLength = typing.Annotated[int, pydantic.Field(ge=2)]  # type: ignore[misc,assignment]
    Temperature0to2 = typing.Annotated[float, pydantic.Field(ge=0, le=2)]  # type: ignore[misc,assignment]
    Temperature0to1 = typing.Annotated[float, pydantic.Field(ge=0, le=1)]  # type: ignore[misc,assignment]
else:
    IntContextLength = pydantic.conint(ge=2)  # type: ignore[attr-defined,misc,assignment,no-redef]
    Temperature0to2 = pydantic.confloat(ge=0, le=2)  # type: ignore[attr-defined,misc,assignment,no-redef]
    Temperature0to1 = pydantic.confloat(ge=0, le=1)  # type: ignore[attr-defined,misc,assignment,no-redef]


class AgentV1AudioInput(UniversalBaseModel):
    """Audio input configuration settings"""
    
    encoding: typing.Literal[
        "linear16", "linear32", "flac", "alaw", "mulaw", 
        "amr-nb", "amr-wb", "opus", "ogg-opus", "speex", "g729"
    ] = "linear16"
    """Audio encoding format"""
    
    sample_rate: int = 24000
    """Sample rate in Hz. Common values are 16000, 24000, 44100, 48000"""

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


class AgentV1AudioOutput(UniversalBaseModel):
    """Audio output configuration settings"""
    
    encoding: typing.Optional[typing.Literal["linear16", "mulaw", "alaw"]] = "linear16"
    """Audio encoding format for streaming TTS output"""
    
    sample_rate: typing.Optional[int] = None
    """Sample rate in Hz"""
    
    bitrate: typing.Optional[int] = None
    """Audio bitrate in bits per second"""
    
    container: typing.Optional[str] = None
    """Audio container format. If omitted, defaults to 'none'"""

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


class AgentV1AudioConfig(UniversalBaseModel):
    """Audio configuration settings"""
    
    input: typing.Optional[AgentV1AudioInput] = None
    """Audio input configuration"""
    
    output: typing.Optional[AgentV1AudioOutput] = None
    """Audio output configuration"""

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


class AgentV1HistoryMessage(UniversalBaseModel):
    """Conversation text as part of the conversation history"""
    
    type: typing.Literal["History"] = "History"
    """Message type identifier for conversation text"""
    
    role: typing.Literal["user", "assistant"]
    """Identifies who spoke the statement"""
    
    content: str
    """The actual statement that was spoken"""

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


class AgentV1FunctionCall(UniversalBaseModel):
    """Function call in conversation history"""
    
    id: str
    """Unique identifier for the function call"""
    
    name: str
    """Name of the function called"""
    
    client_side: bool
    """Indicates if the call was client-side or server-side"""
    
    arguments: str
    """Arguments passed to the function"""
    
    response: str
    """Response from the function call"""

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


class AgentV1HistoryFunctionCalls(UniversalBaseModel):
    """Client-side or server-side function call request and response as part of the conversation history"""
    
    type: typing.Literal["History"] = "History"
    """Message type identifier"""
    
    function_calls: typing.List[AgentV1FunctionCall]
    """List of function call objects"""

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


class AgentV1Flags(UniversalBaseModel):
    """Agent flags configuration"""
    
    history: bool = True
    """Enable or disable history message reporting"""

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


# Context configuration
class AgentV1Context(UniversalBaseModel):
    """Conversation context including the history of messages and function calls"""
    
    messages: typing.Optional[typing.List[typing.Union[AgentV1HistoryMessage, AgentV1HistoryFunctionCalls]]] = None
    """Conversation history as a list of messages and function calls"""

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


# Listen provider configuration
class AgentV1ListenProvider(UniversalBaseModel):
    """Listen provider configuration"""
    
    type: typing.Literal["deepgram"] = "deepgram"
    """Provider type for speech-to-text"""
    
    model: str
    """Model to use for speech to text"""
    
    keyterms: typing.Optional[typing.List[str]] = None
    """Prompt key-term recognition (nova-3 'en' only)"""
    
    smart_format: typing.Optional[bool] = False
    """Applies smart formatting to improve transcript readability (Deepgram providers only)"""

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


class AgentV1Listen(UniversalBaseModel):
    """Listen configuration"""
    
    provider: AgentV1ListenProvider
    """Listen provider configuration"""

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


# Endpoint configuration
class AgentV1Endpoint(UniversalBaseModel):
    """Custom endpoint configuration"""
    
    url: str
    """Custom endpoint URL"""
    
    headers: typing.Optional[typing.Dict[str, str]] = None
    """Custom headers for the endpoint"""

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


# AWS Credentials
class AgentV1AwsCredentials(UniversalBaseModel):
    """AWS credentials configuration"""
    
    type: typing.Literal["sts", "iam"]
    """AWS credentials type (STS short-lived or IAM long-lived)"""
    
    region: str
    """AWS region"""
    
    access_key_id: str
    """AWS access key"""
    
    secret_access_key: str
    """AWS secret access key"""
    
    session_token: typing.Optional[str] = None
    """AWS session token (required for STS only)"""

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


# Function definition
class AgentV1Function(UniversalBaseModel):
    """Function definition for think provider"""
    
    name: str
    """Function name"""
    
    description: typing.Optional[str] = None
    """Function description"""
    
    parameters: typing.Optional[typing.Dict[str, typing.Any]] = None
    """Function parameters"""
    
    endpoint: typing.Optional[AgentV1Endpoint] = None
    """The Function endpoint to call. if not passed, function is called client-side"""

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


# Think provider configurations
class AgentV1OpenAiThinkProvider(UniversalBaseModel):
    """OpenAI think provider configuration"""
    
    type: typing.Literal["open_ai"] = "open_ai"
    """Provider type"""
    
    model: typing.Literal[
        "gpt-5", "gpt-5-mini", "gpt-5-nano", "gpt-4.1", "gpt-4.1-mini", 
        "gpt-4.1-nano", "gpt-4o", "gpt-4o-mini"
    ]
    """OpenAI model to use"""
    
    temperature: typing.Optional[Temperature0to2] = None
    """OpenAI temperature (0-2)"""

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


class AgentV1AwsBedrockThinkProvider(UniversalBaseModel):
    """AWS Bedrock think provider configuration"""
    
    type: typing.Literal["aws_bedrock"] = "aws_bedrock"
    """Provider type"""
    
    model: typing.Literal[
        "anthropic/claude-3-5-sonnet-20240620-v1:0", 
        "anthropic/claude-3-5-haiku-20240307-v1:0"
    ]
    """AWS Bedrock model to use"""
    
    temperature: typing.Optional[Temperature0to2] = None
    """AWS Bedrock temperature (0-2)"""
    
    credentials: typing.Optional[AgentV1AwsCredentials] = None
    """AWS credentials type (STS short-lived or IAM long-lived)"""

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


class AgentV1AnthropicThinkProvider(UniversalBaseModel):
    """Anthropic think provider configuration"""
    
    type: typing.Literal["anthropic"] = "anthropic"
    """Provider type"""
    
    model: typing.Literal["claude-3-5-haiku-latest", "claude-sonnet-4-20250514"]
    """Anthropic model to use"""
    
    temperature: typing.Optional[Temperature0to1] = None
    """Anthropic temperature (0-1)"""

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


class AgentV1GoogleThinkProvider(UniversalBaseModel):
    """Google think provider configuration"""
    
    type: typing.Literal["google"] = "google"
    """Provider type"""
    
    model: typing.Literal["gemini-2.0-flash", "gemini-2.0-flash-lite", "gemini-2.5-flash"]
    """Google model to use"""
    
    temperature: typing.Optional[Temperature0to2] = None
    """Google temperature (0-2)"""

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


class AgentV1GroqThinkProvider(UniversalBaseModel):
    """Groq think provider configuration"""
    
    type: typing.Literal["groq"] = "groq"
    """Provider type"""
    
    model: typing.Literal["openai/gpt-oss-20b"]
    """Groq model to use"""
    
    temperature: typing.Optional[Temperature0to2] = None
    """Groq temperature (0-2)"""

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


# Think configuration
class AgentV1Think(UniversalBaseModel):
    """Think configuration"""
    
    provider: typing.Union[
        AgentV1OpenAiThinkProvider, AgentV1AwsBedrockThinkProvider, 
        AgentV1AnthropicThinkProvider, AgentV1GoogleThinkProvider, 
        AgentV1GroqThinkProvider
    ]
    """Think provider configuration"""
    
    endpoint: typing.Optional[AgentV1Endpoint] = None
    """Optional for non-Deepgram LLM providers. When present, must include url field and headers object"""
    
    functions: typing.Optional[typing.List[AgentV1Function]] = None
    """Function definitions"""
    
    prompt: typing.Optional[str] = None
    """System prompt"""
    
    context_length: typing.Optional[typing.Union[typing.Literal["max"], IntContextLength]] = None
    """Specifies the number of characters retained in context between user messages, agent responses, and function calls"""

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


# Speak provider configurations
class AgentV1DeepgramSpeakProvider(UniversalBaseModel):
    """Deepgram speak provider configuration"""
    
    type: typing.Literal["deepgram"] = "deepgram"
    """Provider type"""
    
    model: typing.Literal[
        # Aura-1 English Voices
        "aura-asteria-en", "aura-luna-en", "aura-stella-en", "aura-athena-en", 
        "aura-hera-en", "aura-orion-en", "aura-arcas-en", "aura-perseus-en", 
        "aura-angus-en", "aura-orpheus-en", "aura-helios-en", "aura-zeus-en",
        # Aura-2 English Voices
        "aura-2-amalthea-en", "aura-2-andromeda-en", "aura-2-apollo-en", 
        "aura-2-arcas-en", "aura-2-aries-en", "aura-2-asteria-en", 
        "aura-2-athena-en", "aura-2-atlas-en", "aura-2-aurora-en", 
        "aura-2-callista-en", "aura-2-cora-en", "aura-2-cordelia-en", 
        "aura-2-delia-en", "aura-2-draco-en", "aura-2-electra-en", 
        "aura-2-harmonia-en", "aura-2-helena-en", "aura-2-hera-en", 
        "aura-2-hermes-en", "aura-2-hyperion-en", "aura-2-iris-en", 
        "aura-2-janus-en", "aura-2-juno-en", "aura-2-jupiter-en", 
        "aura-2-luna-en", "aura-2-mars-en", "aura-2-minerva-en", 
        "aura-2-neptune-en", "aura-2-odysseus-en", "aura-2-ophelia-en", 
        "aura-2-orion-en", "aura-2-orpheus-en", "aura-2-pandora-en", 
        "aura-2-phoebe-en", "aura-2-pluto-en", "aura-2-saturn-en", 
        "aura-2-selene-en", "aura-2-thalia-en", "aura-2-theia-en", 
        "aura-2-vesta-en", "aura-2-zeus-en",
        # Aura-2 Spanish Voices
        "aura-2-sirio-es", "aura-2-nestor-es", "aura-2-carina-es", 
        "aura-2-celeste-es", "aura-2-alvaro-es", "aura-2-diana-es", 
        "aura-2-aquila-es", "aura-2-selena-es", "aura-2-estrella-es", 
        "aura-2-javier-es"
    ]
    """Deepgram TTS model"""

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


class AgentV1ElevenLabsSpeakProvider(UniversalBaseModel):
    """Eleven Labs speak provider configuration"""
    
    type: typing.Literal["eleven_labs"] = "eleven_labs"
    """Provider type"""
    
    model_id: typing.Literal["eleven_turbo_v2_5", "eleven_monolingual_v1", "eleven_multilingual_v2"]
    """Eleven Labs model ID"""
    
    language_code: typing.Optional[str] = None
    """Eleven Labs optional language code"""

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


class AgentV1CartesiaVoice(UniversalBaseModel):
    """Cartesia voice configuration"""
    
    mode: str
    """Cartesia voice mode"""
    
    id: str
    """Cartesia voice ID"""

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


class AgentV1CartesiaSpeakProvider(UniversalBaseModel):
    """Cartesia speak provider configuration"""
    
    type: typing.Literal["cartesia"] = "cartesia"
    """Provider type"""
    
    model_id: typing.Literal["sonic-2", "sonic-multilingual"]
    """Cartesia model ID"""
    
    voice: AgentV1CartesiaVoice
    """Cartesia voice configuration"""
    
    language: typing.Optional[str] = None
    """Cartesia language code"""

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


class AgentV1OpenAiSpeakProvider(UniversalBaseModel):
    """OpenAI speak provider configuration"""
    
    type: typing.Literal["open_ai"] = "open_ai"
    """Provider type"""
    
    model: typing.Literal["tts-1", "tts-1-hd"]
    """OpenAI TTS model"""
    
    voice: typing.Literal["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
    """OpenAI voice"""

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


class AgentV1AwsPollySpeakProvider(UniversalBaseModel):
    """AWS Polly speak provider configuration"""
    
    type: typing.Literal["aws_polly"] = "aws_polly"
    """Provider type"""
    
    voice: typing.Literal["Matthew", "Joanna", "Amy", "Emma", "Brian", "Arthur", "Aria", "Ayanda"]
    """AWS Polly voice name"""
    
    language_code: str
    """Language code (e.g., "en-US")"""
    
    engine: typing.Literal["generative", "long-form", "standard", "neural"]
    """AWS Polly engine"""
    
    credentials: AgentV1AwsCredentials
    """AWS credentials"""

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


# Speak configuration
class AgentV1SpeakProviderConfig(UniversalBaseModel):
    """Speak provider configuration wrapper"""
    
    provider: typing.Union[
        AgentV1DeepgramSpeakProvider, AgentV1ElevenLabsSpeakProvider,
        AgentV1CartesiaSpeakProvider, AgentV1OpenAiSpeakProvider,
        AgentV1AwsPollySpeakProvider
    ]
    """Speak provider configuration"""
    
    endpoint: typing.Optional[AgentV1Endpoint] = None
    """Optional if provider is Deepgram. Required for non-Deepgram TTS providers"""

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow



# Agent configuration
class AgentV1Agent(UniversalBaseModel):
    """Agent configuration"""
    
    language: typing.Optional[typing.Literal["en", "es"]] = "en"
    """Agent language"""
    
    context: typing.Optional[AgentV1Context] = None
    """Conversation context including the history of messages and function calls"""
    
    listen: typing.Optional[AgentV1Listen] = None
    """Listen configuration"""
    
    think: AgentV1Think
    """Think configuration"""
    
    speak: typing.Union[AgentV1SpeakProviderConfig, typing.List[AgentV1SpeakProviderConfig]]
    """Speak configuration - can be single provider or array of providers"""
    
    greeting: typing.Optional[str] = None
    """Optional message that agent will speak at the start"""

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


class AgentV1SettingsMessage(UniversalBaseModel):
    """
    Configure the voice agent and sets the input and output audio formats
    """
    
    type: typing.Literal["Settings"] = "Settings"
    """Message type identifier"""
    
    audio: AgentV1AudioConfig
    """Audio configuration settings"""
    
    agent: AgentV1Agent
    """Agent configuration with proper nested types"""
    
    tags: typing.Optional[typing.List[str]] = None
    """Tags to associate with the request"""
    
    experimental: typing.Optional[bool] = False
    """To enable experimental features"""
    
    flags: typing.Optional[AgentV1Flags] = None
    """Agent flags configuration"""
    
    mip_opt_out: typing.Optional[bool] = False
    """To opt out of Deepgram Model Improvement Program"""

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:
        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow