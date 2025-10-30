# Reference
## Agent V1 Settings Think Models
<details><summary><code>client.agent.v1.settings.think.models.<a href="src/deepgram/agent/v1/settings/think/models/client.py">list</a>()</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieves the available think models that can be used for AI agent processing
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from deepgram import DeepgramClient

client = DeepgramClient(
    api_key="YOUR_API_KEY",
)
client.agent.v1.settings.think.models.list()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Auth V1 Tokens
<details><summary><code>client.auth.v1.tokens.<a href="src/deepgram/auth/v1/tokens/client.py">grant</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Generates a temporary JSON Web Token (JWT) with a 30-second (by default) TTL and usage::write permission for core voice APIs, requiring an API key with Member or higher authorization. Tokens created with this endpoint will not work with the Manage APIs.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from deepgram import DeepgramClient

client = DeepgramClient(
    api_key="YOUR_API_KEY",
)
client.auth.v1.tokens.grant()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**ttl_seconds:** `typing.Optional[float]` — Time to live in seconds for the token. Defaults to 30 seconds.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Listen V1 Media
<details><summary><code>client.listen.v1.media.<a href="src/deepgram/listen/v1/media/client.py">transcribe_url</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Transcribe audio and video using Deepgram's speech-to-text REST API
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from deepgram import DeepgramClient

client = DeepgramClient(
    api_key="YOUR_API_KEY",
)
client.listen.v1.media.transcribe_url(
    url="https://dpgr.am/spacewalk.wav",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**url:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**callback:** `typing.Optional[str]` — URL to which we'll make the callback request
    
</dd>
</dl>

<dl>
<dd>

**callback_method:** `typing.Optional[MediaTranscribeRequestCallbackMethod]` — HTTP method by which the callback request will be made
    
</dd>
</dl>

<dl>
<dd>

**extra:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — Arbitrary key-value pairs that are attached to the API response for usage in downstream processing
    
</dd>
</dl>

<dl>
<dd>

**sentiment:** `typing.Optional[bool]` — Recognizes the sentiment throughout a transcript or text
    
</dd>
</dl>

<dl>
<dd>

**summarize:** `typing.Optional[MediaTranscribeRequestSummarize]` — Summarize content. For Listen API, supports string version option. For Read API, accepts boolean only.
    
</dd>
</dl>

<dl>
<dd>

**tag:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — Label your requests for the purpose of identification during usage reporting
    
</dd>
</dl>

<dl>
<dd>

**topics:** `typing.Optional[bool]` — Detect topics throughout a transcript or text
    
</dd>
</dl>

<dl>
<dd>

**custom_topic:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — Custom topics you want the model to detect within your input audio or text if present Submit up to `100`.
    
</dd>
</dl>

<dl>
<dd>

**custom_topic_mode:** `typing.Optional[MediaTranscribeRequestCustomTopicMode]` — Sets how the model will interpret strings submitted to the `custom_topic` param. When `strict`, the model will only return topics submitted using the `custom_topic` param. When `extended`, the model will return its own detected topics in addition to those submitted using the `custom_topic` param
    
</dd>
</dl>

<dl>
<dd>

**intents:** `typing.Optional[bool]` — Recognizes speaker intent throughout a transcript or text
    
</dd>
</dl>

<dl>
<dd>

**custom_intent:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — Custom intents you want the model to detect within your input audio if present
    
</dd>
</dl>

<dl>
<dd>

**custom_intent_mode:** `typing.Optional[MediaTranscribeRequestCustomIntentMode]` — Sets how the model will interpret intents submitted to the `custom_intent` param. When `strict`, the model will only return intents submitted using the `custom_intent` param. When `extended`, the model will return its own detected intents in the `custom_intent` param.
    
</dd>
</dl>

<dl>
<dd>

**detect_entities:** `typing.Optional[bool]` — Identifies and extracts key entities from content in submitted audio
    
</dd>
</dl>

<dl>
<dd>

**detect_language:** `typing.Optional[bool]` — Identifies the dominant language spoken in submitted audio
    
</dd>
</dl>

<dl>
<dd>

**diarize:** `typing.Optional[bool]` — Recognize speaker changes. Each word in the transcript will be assigned a speaker number starting at 0
    
</dd>
</dl>

<dl>
<dd>

**dictation:** `typing.Optional[bool]` — Dictation mode for controlling formatting with dictated speech
    
</dd>
</dl>

<dl>
<dd>

**encoding:** `typing.Optional[MediaTranscribeRequestEncoding]` — Specify the expected encoding of your submitted audio
    
</dd>
</dl>

<dl>
<dd>

**filler_words:** `typing.Optional[bool]` — Filler Words can help transcribe interruptions in your audio, like "uh" and "um"
    
</dd>
</dl>

<dl>
<dd>

**keyterm:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — Key term prompting can boost or suppress specialized terminology and brands. Only compatible with Nova-3
    
</dd>
</dl>

<dl>
<dd>

**keywords:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — Keywords can boost or suppress specialized terminology and brands
    
</dd>
</dl>

<dl>
<dd>

**language:** `typing.Optional[str]` — The [BCP-47 language tag](https://tools.ietf.org/html/bcp47) that hints at the primary spoken language. Depending on the Model and API endpoint you choose only certain languages are available
    
</dd>
</dl>

<dl>
<dd>

**measurements:** `typing.Optional[bool]` — Spoken measurements will be converted to their corresponding abbreviations
    
</dd>
</dl>

<dl>
<dd>

**model:** `typing.Optional[MediaTranscribeRequestModel]` — AI model used to process submitted audio
    
</dd>
</dl>

<dl>
<dd>

**multichannel:** `typing.Optional[bool]` — Transcribe each audio channel independently
    
</dd>
</dl>

<dl>
<dd>

**numerals:** `typing.Optional[bool]` — Numerals converts numbers from written format to numerical format
    
</dd>
</dl>

<dl>
<dd>

**paragraphs:** `typing.Optional[bool]` — Splits audio into paragraphs to improve transcript readability
    
</dd>
</dl>

<dl>
<dd>

**profanity_filter:** `typing.Optional[bool]` — Profanity Filter looks for recognized profanity and converts it to the nearest recognized non-profane word or removes it from the transcript completely
    
</dd>
</dl>

<dl>
<dd>

**punctuate:** `typing.Optional[bool]` — Add punctuation and capitalization to the transcript
    
</dd>
</dl>

<dl>
<dd>

**redact:** `typing.Optional[str]` — Redaction removes sensitive information from your transcripts
    
</dd>
</dl>

<dl>
<dd>

**replace:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — Search for terms or phrases in submitted audio and replaces them
    
</dd>
</dl>

<dl>
<dd>

**search:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — Search for terms or phrases in submitted audio
    
</dd>
</dl>

<dl>
<dd>

**smart_format:** `typing.Optional[bool]` — Apply formatting to transcript output. When set to true, additional formatting will be applied to transcripts to improve readability
    
</dd>
</dl>

<dl>
<dd>

**utterances:** `typing.Optional[bool]` — Segments speech into meaningful semantic units
    
</dd>
</dl>

<dl>
<dd>

**utt_split:** `typing.Optional[float]` — Seconds to wait before detecting a pause between words in submitted audio
    
</dd>
</dl>

<dl>
<dd>

**version:** `typing.Optional[MediaTranscribeRequestVersion]` — Version of an AI model to use
    
</dd>
</dl>

<dl>
<dd>

**mip_opt_out:** `typing.Optional[bool]` — Opts out requests from the Deepgram Model Improvement Program. Refer to our Docs for pricing impacts before setting this to true. https://dpgr.am/deepgram-mip
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.listen.v1.media.<a href="src/deepgram/listen/v1/media/client.py">transcribe_file</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Transcribe audio and video using Deepgram's speech-to-text REST API
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from deepgram import DeepgramClient

client = DeepgramClient(
    api_key="YOUR_API_KEY",
)
client.listen.v1.media.transcribe_file()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request:** `typing.Union[bytes, typing.Iterator[bytes], typing.AsyncIterator[bytes]]` 
    
</dd>
</dl>

<dl>
<dd>

**callback:** `typing.Optional[str]` — URL to which we'll make the callback request
    
</dd>
</dl>

<dl>
<dd>

**callback_method:** `typing.Optional[MediaTranscribeRequestCallbackMethod]` — HTTP method by which the callback request will be made
    
</dd>
</dl>

<dl>
<dd>

**extra:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — Arbitrary key-value pairs that are attached to the API response for usage in downstream processing
    
</dd>
</dl>

<dl>
<dd>

**sentiment:** `typing.Optional[bool]` — Recognizes the sentiment throughout a transcript or text
    
</dd>
</dl>

<dl>
<dd>

**summarize:** `typing.Optional[MediaTranscribeRequestSummarize]` — Summarize content. For Listen API, supports string version option. For Read API, accepts boolean only.
    
</dd>
</dl>

<dl>
<dd>

**tag:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — Label your requests for the purpose of identification during usage reporting
    
</dd>
</dl>

<dl>
<dd>

**topics:** `typing.Optional[bool]` — Detect topics throughout a transcript or text
    
</dd>
</dl>

<dl>
<dd>

**custom_topic:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — Custom topics you want the model to detect within your input audio or text if present Submit up to `100`.
    
</dd>
</dl>

<dl>
<dd>

**custom_topic_mode:** `typing.Optional[MediaTranscribeRequestCustomTopicMode]` — Sets how the model will interpret strings submitted to the `custom_topic` param. When `strict`, the model will only return topics submitted using the `custom_topic` param. When `extended`, the model will return its own detected topics in addition to those submitted using the `custom_topic` param
    
</dd>
</dl>

<dl>
<dd>

**intents:** `typing.Optional[bool]` — Recognizes speaker intent throughout a transcript or text
    
</dd>
</dl>

<dl>
<dd>

**custom_intent:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — Custom intents you want the model to detect within your input audio if present
    
</dd>
</dl>

<dl>
<dd>

**custom_intent_mode:** `typing.Optional[MediaTranscribeRequestCustomIntentMode]` — Sets how the model will interpret intents submitted to the `custom_intent` param. When `strict`, the model will only return intents submitted using the `custom_intent` param. When `extended`, the model will return its own detected intents in the `custom_intent` param.
    
</dd>
</dl>

<dl>
<dd>

**detect_entities:** `typing.Optional[bool]` — Identifies and extracts key entities from content in submitted audio
    
</dd>
</dl>

<dl>
<dd>

**detect_language:** `typing.Optional[bool]` — Identifies the dominant language spoken in submitted audio
    
</dd>
</dl>

<dl>
<dd>

**diarize:** `typing.Optional[bool]` — Recognize speaker changes. Each word in the transcript will be assigned a speaker number starting at 0
    
</dd>
</dl>

<dl>
<dd>

**dictation:** `typing.Optional[bool]` — Dictation mode for controlling formatting with dictated speech
    
</dd>
</dl>

<dl>
<dd>

**encoding:** `typing.Optional[MediaTranscribeRequestEncoding]` — Specify the expected encoding of your submitted audio
    
</dd>
</dl>

<dl>
<dd>

**filler_words:** `typing.Optional[bool]` — Filler Words can help transcribe interruptions in your audio, like "uh" and "um"
    
</dd>
</dl>

<dl>
<dd>

**keyterm:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — Key term prompting can boost or suppress specialized terminology and brands. Only compatible with Nova-3
    
</dd>
</dl>

<dl>
<dd>

**keywords:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — Keywords can boost or suppress specialized terminology and brands
    
</dd>
</dl>

<dl>
<dd>

**language:** `typing.Optional[str]` — The [BCP-47 language tag](https://tools.ietf.org/html/bcp47) that hints at the primary spoken language. Depending on the Model and API endpoint you choose only certain languages are available
    
</dd>
</dl>

<dl>
<dd>

**measurements:** `typing.Optional[bool]` — Spoken measurements will be converted to their corresponding abbreviations
    
</dd>
</dl>

<dl>
<dd>

**model:** `typing.Optional[MediaTranscribeRequestModel]` — AI model used to process submitted audio
    
</dd>
</dl>

<dl>
<dd>

**multichannel:** `typing.Optional[bool]` — Transcribe each audio channel independently
    
</dd>
</dl>

<dl>
<dd>

**numerals:** `typing.Optional[bool]` — Numerals converts numbers from written format to numerical format
    
</dd>
</dl>

<dl>
<dd>

**paragraphs:** `typing.Optional[bool]` — Splits audio into paragraphs to improve transcript readability
    
</dd>
</dl>

<dl>
<dd>

**profanity_filter:** `typing.Optional[bool]` — Profanity Filter looks for recognized profanity and converts it to the nearest recognized non-profane word or removes it from the transcript completely
    
</dd>
</dl>

<dl>
<dd>

**punctuate:** `typing.Optional[bool]` — Add punctuation and capitalization to the transcript
    
</dd>
</dl>

<dl>
<dd>

**redact:** `typing.Optional[str]` — Redaction removes sensitive information from your transcripts
    
</dd>
</dl>

<dl>
<dd>

**replace:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — Search for terms or phrases in submitted audio and replaces them
    
</dd>
</dl>

<dl>
<dd>

**search:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — Search for terms or phrases in submitted audio
    
</dd>
</dl>

<dl>
<dd>

**smart_format:** `typing.Optional[bool]` — Apply formatting to transcript output. When set to true, additional formatting will be applied to transcripts to improve readability
    
</dd>
</dl>

<dl>
<dd>

**utterances:** `typing.Optional[bool]` — Segments speech into meaningful semantic units
    
</dd>
</dl>

<dl>
<dd>

**utt_split:** `typing.Optional[float]` — Seconds to wait before detecting a pause between words in submitted audio
    
</dd>
</dl>

<dl>
<dd>

**version:** `typing.Optional[MediaTranscribeRequestVersion]` — Version of an AI model to use
    
</dd>
</dl>

<dl>
<dd>

**mip_opt_out:** `typing.Optional[bool]` — Opts out requests from the Deepgram Model Improvement Program. Refer to our Docs for pricing impacts before setting this to true. https://dpgr.am/deepgram-mip
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Manage V1 Models
<details><summary><code>client.manage.v1.models.<a href="src/deepgram/manage/v1/models/client.py">list</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns metadata on all the latest public models. To retrieve custom models, use Get Project Models.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from deepgram import DeepgramClient

client = DeepgramClient(
    api_key="YOUR_API_KEY",
)
client.manage.v1.models.list()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**include_outdated:** `typing.Optional[bool]` — returns non-latest versions of models
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.manage.v1.models.<a href="src/deepgram/manage/v1/models/client.py">get</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns metadata for a specific public model
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from deepgram import DeepgramClient

client = DeepgramClient(
    api_key="YOUR_API_KEY",
)
client.manage.v1.models.get(
    model_id="af6e9977-99f6-4d8f-b6f5-dfdf6fb6e291",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**model_id:** `str` — The specific UUID of the model
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Manage V1 Projects
<details><summary><code>client.manage.v1.projects.<a href="src/deepgram/manage/v1/projects/client.py">list</a>()</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieves basic information about the projects associated with the API key
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from deepgram import DeepgramClient

client = DeepgramClient(
    api_key="YOUR_API_KEY",
)
client.manage.v1.projects.list()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.manage.v1.projects.<a href="src/deepgram/manage/v1/projects/client.py">get</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieves information about the specified project
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from deepgram import DeepgramClient

client = DeepgramClient(
    api_key="YOUR_API_KEY",
)
client.manage.v1.projects.get(
    project_id="123456-7890-1234-5678-901234",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**project_id:** `str` — The unique identifier of the project
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[float]` — Number of results to return per page. Default 10. Range [1,1000]
    
</dd>
</dl>

<dl>
<dd>

**page:** `typing.Optional[float]` — Navigate and return the results to retrieve specific portions of information of the response
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.manage.v1.projects.<a href="src/deepgram/manage/v1/projects/client.py">delete</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Deletes the specified project
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from deepgram import DeepgramClient

client = DeepgramClient(
    api_key="YOUR_API_KEY",
)
client.manage.v1.projects.delete(
    project_id="123456-7890-1234-5678-901234",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**project_id:** `str` — The unique identifier of the project
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.manage.v1.projects.<a href="src/deepgram/manage/v1/projects/client.py">update</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Updates the name or other properties of an existing project
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from deepgram import DeepgramClient

client = DeepgramClient(
    api_key="YOUR_API_KEY",
)
client.manage.v1.projects.update(
    project_id="123456-7890-1234-5678-901234",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**project_id:** `str` — The unique identifier of the project
    
</dd>
</dl>

<dl>
<dd>

**name:** `typing.Optional[str]` — The name of the project
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.manage.v1.projects.<a href="src/deepgram/manage/v1/projects/client.py">leave</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Removes the authenticated account from the specific project
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from deepgram import DeepgramClient

client = DeepgramClient(
    api_key="YOUR_API_KEY",
)
client.manage.v1.projects.leave(
    project_id="123456-7890-1234-5678-901234",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**project_id:** `str` — The unique identifier of the project
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Manage V1 Projects Keys
<details><summary><code>client.manage.v1.projects.keys.<a href="src/deepgram/manage/v1/projects/keys/client.py">list</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieves all API keys associated with the specified project
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from deepgram import DeepgramClient

client = DeepgramClient(
    api_key="YOUR_API_KEY",
)
client.manage.v1.projects.keys.list(
    project_id="123456-7890-1234-5678-901234",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**project_id:** `str` — The unique identifier of the project
    
</dd>
</dl>

<dl>
<dd>

**status:** `typing.Optional[KeysListRequestStatus]` — Only return keys with a specific status
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.manage.v1.projects.keys.<a href="src/deepgram/manage/v1/projects/keys/client.py">create</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Creates a new API key with specified settings for the project
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from deepgram import DeepgramClient

client = DeepgramClient(
    api_key="YOUR_API_KEY",
)
client.manage.v1.projects.keys.create(
    project_id="project_id",
    request={"key": "value"},
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**project_id:** `str` — The unique identifier of the project
    
</dd>
</dl>

<dl>
<dd>

**request:** `CreateKeyV1RequestOne` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.manage.v1.projects.keys.<a href="src/deepgram/manage/v1/projects/keys/client.py">get</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieves information about a specified API key
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from deepgram import DeepgramClient

client = DeepgramClient(
    api_key="YOUR_API_KEY",
)
client.manage.v1.projects.keys.get(
    project_id="123456-7890-1234-5678-901234",
    key_id="123456789012345678901234",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**project_id:** `str` — The unique identifier of the project
    
</dd>
</dl>

<dl>
<dd>

**key_id:** `str` — The unique identifier of the API key
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.manage.v1.projects.keys.<a href="src/deepgram/manage/v1/projects/keys/client.py">delete</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Deletes an API key for a specific project
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from deepgram import DeepgramClient

client = DeepgramClient(
    api_key="YOUR_API_KEY",
)
client.manage.v1.projects.keys.delete(
    project_id="123456-7890-1234-5678-901234",
    key_id="123456789012345678901234",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**project_id:** `str` — The unique identifier of the project
    
</dd>
</dl>

<dl>
<dd>

**key_id:** `str` — The unique identifier of the API key
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Manage V1 Projects Members
<details><summary><code>client.manage.v1.projects.members.<a href="src/deepgram/manage/v1/projects/members/client.py">list</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieves a list of members for a given project
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from deepgram import DeepgramClient

client = DeepgramClient(
    api_key="YOUR_API_KEY",
)
client.manage.v1.projects.members.list(
    project_id="123456-7890-1234-5678-901234",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**project_id:** `str` — The unique identifier of the project
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.manage.v1.projects.members.<a href="src/deepgram/manage/v1/projects/members/client.py">delete</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Removes a member from the project using their unique member ID
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from deepgram import DeepgramClient

client = DeepgramClient(
    api_key="YOUR_API_KEY",
)
client.manage.v1.projects.members.delete(
    project_id="123456-7890-1234-5678-901234",
    member_id="123456789012345678901234",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**project_id:** `str` — The unique identifier of the project
    
</dd>
</dl>

<dl>
<dd>

**member_id:** `str` — The unique identifier of the Member
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Manage V1 Projects Models
<details><summary><code>client.manage.v1.projects.models.<a href="src/deepgram/manage/v1/projects/models/client.py">list</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns metadata on all the latest models that a specific project has access to, including non-public models
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from deepgram import DeepgramClient

client = DeepgramClient(
    api_key="YOUR_API_KEY",
)
client.manage.v1.projects.models.list(
    project_id="123456-7890-1234-5678-901234",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**project_id:** `str` — The unique identifier of the project
    
</dd>
</dl>

<dl>
<dd>

**include_outdated:** `typing.Optional[bool]` — returns non-latest versions of models
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.manage.v1.projects.models.<a href="src/deepgram/manage/v1/projects/models/client.py">get</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns metadata for a specific model
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from deepgram import DeepgramClient

client = DeepgramClient(
    api_key="YOUR_API_KEY",
)
client.manage.v1.projects.models.get(
    project_id="123456-7890-1234-5678-901234",
    model_id="af6e9977-99f6-4d8f-b6f5-dfdf6fb6e291",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**project_id:** `str` — The unique identifier of the project
    
</dd>
</dl>

<dl>
<dd>

**model_id:** `str` — The specific UUID of the model
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Manage V1 Projects Requests
<details><summary><code>client.manage.v1.projects.requests.<a href="src/deepgram/manage/v1/projects/requests/client.py">list</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Generates a list of requests for a specific project
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from deepgram import DeepgramClient

client = DeepgramClient(
    api_key="YOUR_API_KEY",
)
client.manage.v1.projects.requests.list(
    project_id="123456-7890-1234-5678-901234",
    accessor="12345678-1234-1234-1234-123456789012",
    request_id="12345678-1234-1234-1234-123456789012",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**project_id:** `str` — The unique identifier of the project
    
</dd>
</dl>

<dl>
<dd>

**start:** `typing.Optional[dt.datetime]` — Start date of the requested date range. Formats accepted are YYYY-MM-DD, YYYY-MM-DDTHH:MM:SS, or YYYY-MM-DDTHH:MM:SS+HH:MM
    
</dd>
</dl>

<dl>
<dd>

**end:** `typing.Optional[dt.datetime]` — End date of the requested date range. Formats accepted are YYYY-MM-DD, YYYY-MM-DDTHH:MM:SS, or YYYY-MM-DDTHH:MM:SS+HH:MM
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[float]` — Number of results to return per page. Default 10. Range [1,1000]
    
</dd>
</dl>

<dl>
<dd>

**page:** `typing.Optional[float]` — Navigate and return the results to retrieve specific portions of information of the response
    
</dd>
</dl>

<dl>
<dd>

**accessor:** `typing.Optional[str]` — Filter for requests where a specific accessor was used
    
</dd>
</dl>

<dl>
<dd>

**request_id:** `typing.Optional[str]` — Filter for a specific request id
    
</dd>
</dl>

<dl>
<dd>

**deployment:** `typing.Optional[RequestsListRequestDeployment]` — Filter for requests where a specific deployment was used
    
</dd>
</dl>

<dl>
<dd>

**endpoint:** `typing.Optional[RequestsListRequestEndpoint]` — Filter for requests where a specific endpoint was used
    
</dd>
</dl>

<dl>
<dd>

**method:** `typing.Optional[RequestsListRequestMethod]` — Filter for requests where a specific method was used
    
</dd>
</dl>

<dl>
<dd>

**status:** `typing.Optional[RequestsListRequestStatus]` — Filter for requests that succeeded (status code < 300) or failed (status code >=400)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.manage.v1.projects.requests.<a href="src/deepgram/manage/v1/projects/requests/client.py">get</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieves a specific request for a specific project
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from deepgram import DeepgramClient

client = DeepgramClient(
    api_key="YOUR_API_KEY",
)
client.manage.v1.projects.requests.get(
    project_id="123456-7890-1234-5678-901234",
    request_id="123456-7890-1234-5678-901234",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**project_id:** `str` — The unique identifier of the project
    
</dd>
</dl>

<dl>
<dd>

**request_id:** `str` — The unique identifier of the request
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Manage V1 Projects Usage
<details><summary><code>client.manage.v1.projects.usage.<a href="src/deepgram/manage/v1/projects/usage/client.py">get</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieves the usage for a specific project. Use Get Project Usage Breakdown for a more comprehensive usage summary.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from deepgram import DeepgramClient

client = DeepgramClient(
    api_key="YOUR_API_KEY",
)
client.manage.v1.projects.usage.get(
    project_id="123456-7890-1234-5678-901234",
    accessor="12345678-1234-1234-1234-123456789012",
    model="6f548761-c9c0-429a-9315-11a1d28499c8",
    sample_rate=True,
    tag="tag1",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**project_id:** `str` — The unique identifier of the project
    
</dd>
</dl>

<dl>
<dd>

**start:** `typing.Optional[str]` — Start date of the requested date range. Format accepted is YYYY-MM-DD
    
</dd>
</dl>

<dl>
<dd>

**end:** `typing.Optional[str]` — End date of the requested date range. Format accepted is YYYY-MM-DD
    
</dd>
</dl>

<dl>
<dd>

**accessor:** `typing.Optional[str]` — Filter for requests where a specific accessor was used
    
</dd>
</dl>

<dl>
<dd>

**alternatives:** `typing.Optional[bool]` — Filter for requests where alternatives were used
    
</dd>
</dl>

<dl>
<dd>

**callback_method:** `typing.Optional[bool]` — Filter for requests where callback method was used
    
</dd>
</dl>

<dl>
<dd>

**callback:** `typing.Optional[bool]` — Filter for requests where callback was used
    
</dd>
</dl>

<dl>
<dd>

**channels:** `typing.Optional[bool]` — Filter for requests where channels were used
    
</dd>
</dl>

<dl>
<dd>

**custom_intent_mode:** `typing.Optional[bool]` — Filter for requests where custom intent mode was used
    
</dd>
</dl>

<dl>
<dd>

**custom_intent:** `typing.Optional[bool]` — Filter for requests where custom intent was used
    
</dd>
</dl>

<dl>
<dd>

**custom_topic_mode:** `typing.Optional[bool]` — Filter for requests where custom topic mode was used
    
</dd>
</dl>

<dl>
<dd>

**custom_topic:** `typing.Optional[bool]` — Filter for requests where custom topic was used
    
</dd>
</dl>

<dl>
<dd>

**deployment:** `typing.Optional[UsageGetRequestDeployment]` — Filter for requests where a specific deployment was used
    
</dd>
</dl>

<dl>
<dd>

**detect_entities:** `typing.Optional[bool]` — Filter for requests where detect entities was used
    
</dd>
</dl>

<dl>
<dd>

**detect_language:** `typing.Optional[bool]` — Filter for requests where detect language was used
    
</dd>
</dl>

<dl>
<dd>

**diarize:** `typing.Optional[bool]` — Filter for requests where diarize was used
    
</dd>
</dl>

<dl>
<dd>

**dictation:** `typing.Optional[bool]` — Filter for requests where dictation was used
    
</dd>
</dl>

<dl>
<dd>

**encoding:** `typing.Optional[bool]` — Filter for requests where encoding was used
    
</dd>
</dl>

<dl>
<dd>

**endpoint:** `typing.Optional[UsageGetRequestEndpoint]` — Filter for requests where a specific endpoint was used
    
</dd>
</dl>

<dl>
<dd>

**extra:** `typing.Optional[bool]` — Filter for requests where extra was used
    
</dd>
</dl>

<dl>
<dd>

**filler_words:** `typing.Optional[bool]` — Filter for requests where filler words was used
    
</dd>
</dl>

<dl>
<dd>

**intents:** `typing.Optional[bool]` — Filter for requests where intents was used
    
</dd>
</dl>

<dl>
<dd>

**keyterm:** `typing.Optional[bool]` — Filter for requests where keyterm was used
    
</dd>
</dl>

<dl>
<dd>

**keywords:** `typing.Optional[bool]` — Filter for requests where keywords was used
    
</dd>
</dl>

<dl>
<dd>

**language:** `typing.Optional[bool]` — Filter for requests where language was used
    
</dd>
</dl>

<dl>
<dd>

**measurements:** `typing.Optional[bool]` — Filter for requests where measurements were used
    
</dd>
</dl>

<dl>
<dd>

**method:** `typing.Optional[UsageGetRequestMethod]` — Filter for requests where a specific method was used
    
</dd>
</dl>

<dl>
<dd>

**model:** `typing.Optional[str]` — Filter for requests where a specific model uuid was used
    
</dd>
</dl>

<dl>
<dd>

**multichannel:** `typing.Optional[bool]` — Filter for requests where multichannel was used
    
</dd>
</dl>

<dl>
<dd>

**numerals:** `typing.Optional[bool]` — Filter for requests where numerals were used
    
</dd>
</dl>

<dl>
<dd>

**paragraphs:** `typing.Optional[bool]` — Filter for requests where paragraphs were used
    
</dd>
</dl>

<dl>
<dd>

**profanity_filter:** `typing.Optional[bool]` — Filter for requests where profanity filter was used
    
</dd>
</dl>

<dl>
<dd>

**punctuate:** `typing.Optional[bool]` — Filter for requests where punctuate was used
    
</dd>
</dl>

<dl>
<dd>

**redact:** `typing.Optional[bool]` — Filter for requests where redact was used
    
</dd>
</dl>

<dl>
<dd>

**replace:** `typing.Optional[bool]` — Filter for requests where replace was used
    
</dd>
</dl>

<dl>
<dd>

**sample_rate:** `typing.Optional[bool]` — Filter for requests where sample rate was used
    
</dd>
</dl>

<dl>
<dd>

**search:** `typing.Optional[bool]` — Filter for requests where search was used
    
</dd>
</dl>

<dl>
<dd>

**sentiment:** `typing.Optional[bool]` — Filter for requests where sentiment was used
    
</dd>
</dl>

<dl>
<dd>

**smart_format:** `typing.Optional[bool]` — Filter for requests where smart format was used
    
</dd>
</dl>

<dl>
<dd>

**summarize:** `typing.Optional[bool]` — Filter for requests where summarize was used
    
</dd>
</dl>

<dl>
<dd>

**tag:** `typing.Optional[str]` — Filter for requests where a specific tag was used
    
</dd>
</dl>

<dl>
<dd>

**topics:** `typing.Optional[bool]` — Filter for requests where topics was used
    
</dd>
</dl>

<dl>
<dd>

**utt_split:** `typing.Optional[bool]` — Filter for requests where utt split was used
    
</dd>
</dl>

<dl>
<dd>

**utterances:** `typing.Optional[bool]` — Filter for requests where utterances was used
    
</dd>
</dl>

<dl>
<dd>

**version:** `typing.Optional[bool]` — Filter for requests where version was used
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Manage V1 Projects Billing Balances
<details><summary><code>client.manage.v1.projects.billing.balances.<a href="src/deepgram/manage/v1/projects/billing/balances/client.py">list</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Generates a list of outstanding balances for the specified project
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from deepgram import DeepgramClient

client = DeepgramClient(
    api_key="YOUR_API_KEY",
)
client.manage.v1.projects.billing.balances.list(
    project_id="123456-7890-1234-5678-901234",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**project_id:** `str` — The unique identifier of the project
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.manage.v1.projects.billing.balances.<a href="src/deepgram/manage/v1/projects/billing/balances/client.py">get</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieves details about the specified balance
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from deepgram import DeepgramClient

client = DeepgramClient(
    api_key="YOUR_API_KEY",
)
client.manage.v1.projects.billing.balances.get(
    project_id="123456-7890-1234-5678-901234",
    balance_id="123456-7890-1234-5678-901234",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**project_id:** `str` — The unique identifier of the project
    
</dd>
</dl>

<dl>
<dd>

**balance_id:** `str` — The unique identifier of the balance
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Manage V1 Projects Billing Breakdown
<details><summary><code>client.manage.v1.projects.billing.breakdown.<a href="src/deepgram/manage/v1/projects/billing/breakdown/client.py">list</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieves the billing summary for a specific project, with various filter options or by grouping options.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from deepgram import DeepgramClient

client = DeepgramClient(
    api_key="YOUR_API_KEY",
)
client.manage.v1.projects.billing.breakdown.list(
    project_id="123456-7890-1234-5678-901234",
    accessor="12345678-1234-1234-1234-123456789012",
    tag="tag1",
    line_item="streaming::nova-3",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**project_id:** `str` — The unique identifier of the project
    
</dd>
</dl>

<dl>
<dd>

**start:** `typing.Optional[str]` — Start date of the requested date range. Format accepted is YYYY-MM-DD
    
</dd>
</dl>

<dl>
<dd>

**end:** `typing.Optional[str]` — End date of the requested date range. Format accepted is YYYY-MM-DD
    
</dd>
</dl>

<dl>
<dd>

**accessor:** `typing.Optional[str]` — Filter for requests where a specific accessor was used
    
</dd>
</dl>

<dl>
<dd>

**deployment:** `typing.Optional[BreakdownListRequestDeployment]` — Filter for requests where a specific deployment was used
    
</dd>
</dl>

<dl>
<dd>

**tag:** `typing.Optional[str]` — Filter for requests where a specific tag was used
    
</dd>
</dl>

<dl>
<dd>

**line_item:** `typing.Optional[str]` — Filter requests by line item (e.g. streaming::nova-3)
    
</dd>
</dl>

<dl>
<dd>

**grouping:** `typing.Optional[
    typing.Union[
        BreakdownListRequestGroupingItem,
        typing.Sequence[BreakdownListRequestGroupingItem],
    ]
]` — Group billing breakdown by one or more dimensions (accessor, deployment, line_item, tags)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Manage V1 Projects Billing Fields
<details><summary><code>client.manage.v1.projects.billing.fields.<a href="src/deepgram/manage/v1/projects/billing/fields/client.py">list</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Lists the accessors, deployment types, tags, and line items used for billing data in the specified time period. Use this endpoint if you want to filter your results from the Billing Breakdown endpoint and want to know what filters are available.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from deepgram import DeepgramClient

client = DeepgramClient(
    api_key="YOUR_API_KEY",
)
client.manage.v1.projects.billing.fields.list(
    project_id="123456-7890-1234-5678-901234",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**project_id:** `str` — The unique identifier of the project
    
</dd>
</dl>

<dl>
<dd>

**start:** `typing.Optional[str]` — Start date of the requested date range. Format accepted is YYYY-MM-DD
    
</dd>
</dl>

<dl>
<dd>

**end:** `typing.Optional[str]` — End date of the requested date range. Format accepted is YYYY-MM-DD
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Manage V1 Projects Billing Purchases
<details><summary><code>client.manage.v1.projects.billing.purchases.<a href="src/deepgram/manage/v1/projects/billing/purchases/client.py">list</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns the original purchased amount on an order transaction
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from deepgram import DeepgramClient

client = DeepgramClient(
    api_key="YOUR_API_KEY",
)
client.manage.v1.projects.billing.purchases.list(
    project_id="123456-7890-1234-5678-901234",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**project_id:** `str` — The unique identifier of the project
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[float]` — Number of results to return per page. Default 10. Range [1,1000]
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Manage V1 Projects Members Invites
<details><summary><code>client.manage.v1.projects.members.invites.<a href="src/deepgram/manage/v1/projects/members/invites/client.py">list</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Generates a list of invites for a specific project
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from deepgram import DeepgramClient

client = DeepgramClient(
    api_key="YOUR_API_KEY",
)
client.manage.v1.projects.members.invites.list(
    project_id="123456-7890-1234-5678-901234",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**project_id:** `str` — The unique identifier of the project
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.manage.v1.projects.members.invites.<a href="src/deepgram/manage/v1/projects/members/invites/client.py">create</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Generates an invite for a specific project
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from deepgram import DeepgramClient

client = DeepgramClient(
    api_key="YOUR_API_KEY",
)
client.manage.v1.projects.members.invites.create(
    project_id="123456-7890-1234-5678-901234",
    email="email",
    scope="scope",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**project_id:** `str` — The unique identifier of the project
    
</dd>
</dl>

<dl>
<dd>

**email:** `str` — The email address of the invitee
    
</dd>
</dl>

<dl>
<dd>

**scope:** `str` — The scope of the invitee
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.manage.v1.projects.members.invites.<a href="src/deepgram/manage/v1/projects/members/invites/client.py">delete</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Deletes an invite for a specific project
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from deepgram import DeepgramClient

client = DeepgramClient(
    api_key="YOUR_API_KEY",
)
client.manage.v1.projects.members.invites.delete(
    project_id="123456-7890-1234-5678-901234",
    email="john.doe@example.com",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**project_id:** `str` — The unique identifier of the project
    
</dd>
</dl>

<dl>
<dd>

**email:** `str` — The email address of the member
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Manage V1 Projects Members Scopes
<details><summary><code>client.manage.v1.projects.members.scopes.<a href="src/deepgram/manage/v1/projects/members/scopes/client.py">list</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieves a list of scopes for a specific member
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from deepgram import DeepgramClient

client = DeepgramClient(
    api_key="YOUR_API_KEY",
)
client.manage.v1.projects.members.scopes.list(
    project_id="123456-7890-1234-5678-901234",
    member_id="123456789012345678901234",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**project_id:** `str` — The unique identifier of the project
    
</dd>
</dl>

<dl>
<dd>

**member_id:** `str` — The unique identifier of the Member
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.manage.v1.projects.members.scopes.<a href="src/deepgram/manage/v1/projects/members/scopes/client.py">update</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Updates the scopes for a specific member
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from deepgram import DeepgramClient

client = DeepgramClient(
    api_key="YOUR_API_KEY",
)
client.manage.v1.projects.members.scopes.update(
    project_id="123456-7890-1234-5678-901234",
    member_id="123456789012345678901234",
    scope="admin",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**project_id:** `str` — The unique identifier of the project
    
</dd>
</dl>

<dl>
<dd>

**member_id:** `str` — The unique identifier of the Member
    
</dd>
</dl>

<dl>
<dd>

**scope:** `str` — A scope to update
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Manage V1 Projects Usage Breakdown
<details><summary><code>client.manage.v1.projects.usage.breakdown.<a href="src/deepgram/manage/v1/projects/usage/breakdown/client.py">get</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieves the usage breakdown for a specific project, with various filter options by API feature or by groupings. Setting a feature (e.g. diarize) to true includes requests that used that feature, while false excludes requests that used it. Multiple true filters are combined with OR logic, while false filters use AND logic.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from deepgram import DeepgramClient

client = DeepgramClient(
    api_key="YOUR_API_KEY",
)
client.manage.v1.projects.usage.breakdown.get(
    project_id="123456-7890-1234-5678-901234",
    accessor="12345678-1234-1234-1234-123456789012",
    model="6f548761-c9c0-429a-9315-11a1d28499c8",
    sample_rate=True,
    tag="tag1",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**project_id:** `str` — The unique identifier of the project
    
</dd>
</dl>

<dl>
<dd>

**start:** `typing.Optional[str]` — Start date of the requested date range. Format accepted is YYYY-MM-DD
    
</dd>
</dl>

<dl>
<dd>

**end:** `typing.Optional[str]` — End date of the requested date range. Format accepted is YYYY-MM-DD
    
</dd>
</dl>

<dl>
<dd>

**grouping:** `typing.Optional[BreakdownGetRequestGrouping]` — Common usage grouping parameters
    
</dd>
</dl>

<dl>
<dd>

**accessor:** `typing.Optional[str]` — Filter for requests where a specific accessor was used
    
</dd>
</dl>

<dl>
<dd>

**alternatives:** `typing.Optional[bool]` — Filter for requests where alternatives were used
    
</dd>
</dl>

<dl>
<dd>

**callback_method:** `typing.Optional[bool]` — Filter for requests where callback method was used
    
</dd>
</dl>

<dl>
<dd>

**callback:** `typing.Optional[bool]` — Filter for requests where callback was used
    
</dd>
</dl>

<dl>
<dd>

**channels:** `typing.Optional[bool]` — Filter for requests where channels were used
    
</dd>
</dl>

<dl>
<dd>

**custom_intent_mode:** `typing.Optional[bool]` — Filter for requests where custom intent mode was used
    
</dd>
</dl>

<dl>
<dd>

**custom_intent:** `typing.Optional[bool]` — Filter for requests where custom intent was used
    
</dd>
</dl>

<dl>
<dd>

**custom_topic_mode:** `typing.Optional[bool]` — Filter for requests where custom topic mode was used
    
</dd>
</dl>

<dl>
<dd>

**custom_topic:** `typing.Optional[bool]` — Filter for requests where custom topic was used
    
</dd>
</dl>

<dl>
<dd>

**deployment:** `typing.Optional[BreakdownGetRequestDeployment]` — Filter for requests where a specific deployment was used
    
</dd>
</dl>

<dl>
<dd>

**detect_entities:** `typing.Optional[bool]` — Filter for requests where detect entities was used
    
</dd>
</dl>

<dl>
<dd>

**detect_language:** `typing.Optional[bool]` — Filter for requests where detect language was used
    
</dd>
</dl>

<dl>
<dd>

**diarize:** `typing.Optional[bool]` — Filter for requests where diarize was used
    
</dd>
</dl>

<dl>
<dd>

**dictation:** `typing.Optional[bool]` — Filter for requests where dictation was used
    
</dd>
</dl>

<dl>
<dd>

**encoding:** `typing.Optional[bool]` — Filter for requests where encoding was used
    
</dd>
</dl>

<dl>
<dd>

**endpoint:** `typing.Optional[BreakdownGetRequestEndpoint]` — Filter for requests where a specific endpoint was used
    
</dd>
</dl>

<dl>
<dd>

**extra:** `typing.Optional[bool]` — Filter for requests where extra was used
    
</dd>
</dl>

<dl>
<dd>

**filler_words:** `typing.Optional[bool]` — Filter for requests where filler words was used
    
</dd>
</dl>

<dl>
<dd>

**intents:** `typing.Optional[bool]` — Filter for requests where intents was used
    
</dd>
</dl>

<dl>
<dd>

**keyterm:** `typing.Optional[bool]` — Filter for requests where keyterm was used
    
</dd>
</dl>

<dl>
<dd>

**keywords:** `typing.Optional[bool]` — Filter for requests where keywords was used
    
</dd>
</dl>

<dl>
<dd>

**language:** `typing.Optional[bool]` — Filter for requests where language was used
    
</dd>
</dl>

<dl>
<dd>

**measurements:** `typing.Optional[bool]` — Filter for requests where measurements were used
    
</dd>
</dl>

<dl>
<dd>

**method:** `typing.Optional[BreakdownGetRequestMethod]` — Filter for requests where a specific method was used
    
</dd>
</dl>

<dl>
<dd>

**model:** `typing.Optional[str]` — Filter for requests where a specific model uuid was used
    
</dd>
</dl>

<dl>
<dd>

**multichannel:** `typing.Optional[bool]` — Filter for requests where multichannel was used
    
</dd>
</dl>

<dl>
<dd>

**numerals:** `typing.Optional[bool]` — Filter for requests where numerals were used
    
</dd>
</dl>

<dl>
<dd>

**paragraphs:** `typing.Optional[bool]` — Filter for requests where paragraphs were used
    
</dd>
</dl>

<dl>
<dd>

**profanity_filter:** `typing.Optional[bool]` — Filter for requests where profanity filter was used
    
</dd>
</dl>

<dl>
<dd>

**punctuate:** `typing.Optional[bool]` — Filter for requests where punctuate was used
    
</dd>
</dl>

<dl>
<dd>

**redact:** `typing.Optional[bool]` — Filter for requests where redact was used
    
</dd>
</dl>

<dl>
<dd>

**replace:** `typing.Optional[bool]` — Filter for requests where replace was used
    
</dd>
</dl>

<dl>
<dd>

**sample_rate:** `typing.Optional[bool]` — Filter for requests where sample rate was used
    
</dd>
</dl>

<dl>
<dd>

**search:** `typing.Optional[bool]` — Filter for requests where search was used
    
</dd>
</dl>

<dl>
<dd>

**sentiment:** `typing.Optional[bool]` — Filter for requests where sentiment was used
    
</dd>
</dl>

<dl>
<dd>

**smart_format:** `typing.Optional[bool]` — Filter for requests where smart format was used
    
</dd>
</dl>

<dl>
<dd>

**summarize:** `typing.Optional[bool]` — Filter for requests where summarize was used
    
</dd>
</dl>

<dl>
<dd>

**tag:** `typing.Optional[str]` — Filter for requests where a specific tag was used
    
</dd>
</dl>

<dl>
<dd>

**topics:** `typing.Optional[bool]` — Filter for requests where topics was used
    
</dd>
</dl>

<dl>
<dd>

**utt_split:** `typing.Optional[bool]` — Filter for requests where utt split was used
    
</dd>
</dl>

<dl>
<dd>

**utterances:** `typing.Optional[bool]` — Filter for requests where utterances was used
    
</dd>
</dl>

<dl>
<dd>

**version:** `typing.Optional[bool]` — Filter for requests where version was used
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Manage V1 Projects Usage Fields
<details><summary><code>client.manage.v1.projects.usage.fields.<a href="src/deepgram/manage/v1/projects/usage/fields/client.py">list</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Lists the features, models, tags, languages, and processing method used for requests in the specified project
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from deepgram import DeepgramClient

client = DeepgramClient(
    api_key="YOUR_API_KEY",
)
client.manage.v1.projects.usage.fields.list(
    project_id="123456-7890-1234-5678-901234",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**project_id:** `str` — The unique identifier of the project
    
</dd>
</dl>

<dl>
<dd>

**start:** `typing.Optional[str]` — Start date of the requested date range. Format accepted is YYYY-MM-DD
    
</dd>
</dl>

<dl>
<dd>

**end:** `typing.Optional[str]` — End date of the requested date range. Format accepted is YYYY-MM-DD
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Read V1 Text
<details><summary><code>client.read.v1.text.<a href="src/deepgram/read/v1/text/client.py">analyze</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Analyze text content using Deepgrams text analysis API
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from deepgram import DeepgramClient

client = DeepgramClient(
    api_key="YOUR_API_KEY",
)
client.read.v1.text.analyze(
    request={"url": "url"},
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request:** `ReadV1RequestParams` 
    
</dd>
</dl>

<dl>
<dd>

**callback:** `typing.Optional[str]` — URL to which we'll make the callback request
    
</dd>
</dl>

<dl>
<dd>

**callback_method:** `typing.Optional[TextAnalyzeRequestCallbackMethod]` — HTTP method by which the callback request will be made
    
</dd>
</dl>

<dl>
<dd>

**sentiment:** `typing.Optional[bool]` — Recognizes the sentiment throughout a transcript or text
    
</dd>
</dl>

<dl>
<dd>

**summarize:** `typing.Optional[TextAnalyzeRequestSummarize]` — Summarize content. For Listen API, supports string version option. For Read API, accepts boolean only.
    
</dd>
</dl>

<dl>
<dd>

**tag:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — Label your requests for the purpose of identification during usage reporting
    
</dd>
</dl>

<dl>
<dd>

**topics:** `typing.Optional[bool]` — Detect topics throughout a transcript or text
    
</dd>
</dl>

<dl>
<dd>

**custom_topic:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — Custom topics you want the model to detect within your input audio or text if present Submit up to `100`.
    
</dd>
</dl>

<dl>
<dd>

**custom_topic_mode:** `typing.Optional[TextAnalyzeRequestCustomTopicMode]` — Sets how the model will interpret strings submitted to the `custom_topic` param. When `strict`, the model will only return topics submitted using the `custom_topic` param. When `extended`, the model will return its own detected topics in addition to those submitted using the `custom_topic` param
    
</dd>
</dl>

<dl>
<dd>

**intents:** `typing.Optional[bool]` — Recognizes speaker intent throughout a transcript or text
    
</dd>
</dl>

<dl>
<dd>

**custom_intent:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — Custom intents you want the model to detect within your input audio if present
    
</dd>
</dl>

<dl>
<dd>

**custom_intent_mode:** `typing.Optional[TextAnalyzeRequestCustomIntentMode]` — Sets how the model will interpret intents submitted to the `custom_intent` param. When `strict`, the model will only return intents submitted using the `custom_intent` param. When `extended`, the model will return its own detected intents in the `custom_intent` param.
    
</dd>
</dl>

<dl>
<dd>

**language:** `typing.Optional[str]` — The [BCP-47 language tag](https://tools.ietf.org/html/bcp47) that hints at the primary spoken language. Depending on the Model and API endpoint you choose only certain languages are available
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## SelfHosted V1 DistributionCredentials
<details><summary><code>client.self_hosted.v1.distribution_credentials.<a href="src/deepgram/self_hosted/v1/distribution_credentials/client.py">list</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Lists sets of distribution credentials for the specified project
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from deepgram import DeepgramClient

client = DeepgramClient(
    api_key="YOUR_API_KEY",
)
client.self_hosted.v1.distribution_credentials.list(
    project_id="123456-7890-1234-5678-901234",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**project_id:** `str` — The unique identifier of the project
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.self_hosted.v1.distribution_credentials.<a href="src/deepgram/self_hosted/v1/distribution_credentials/client.py">create</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Creates a set of distribution credentials for the specified project
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from deepgram import DeepgramClient

client = DeepgramClient(
    api_key="YOUR_API_KEY",
)
client.self_hosted.v1.distribution_credentials.create(
    project_id="123456-7890-1234-5678-901234",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**project_id:** `str` — The unique identifier of the project
    
</dd>
</dl>

<dl>
<dd>

**scopes:** `typing.Optional[
    typing.Union[
        DistributionCredentialsCreateRequestScopesItem,
        typing.Sequence[DistributionCredentialsCreateRequestScopesItem],
    ]
]` — List of permission scopes for the credentials
    
</dd>
</dl>

<dl>
<dd>

**provider:** `typing.Optional[typing.Literal["quay"]]` — The provider of the distribution service
    
</dd>
</dl>

<dl>
<dd>

**comment:** `typing.Optional[str]` — Optional comment about the credentials
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.self_hosted.v1.distribution_credentials.<a href="src/deepgram/self_hosted/v1/distribution_credentials/client.py">get</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns a set of distribution credentials for the specified project
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from deepgram import DeepgramClient

client = DeepgramClient(
    api_key="YOUR_API_KEY",
)
client.self_hosted.v1.distribution_credentials.get(
    project_id="123456-7890-1234-5678-901234",
    distribution_credentials_id="8b36cfd0-472f-4a21-833f-2d6343c3a2f3",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**project_id:** `str` — The unique identifier of the project
    
</dd>
</dl>

<dl>
<dd>

**distribution_credentials_id:** `str` — The UUID of the distribution credentials
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.self_hosted.v1.distribution_credentials.<a href="src/deepgram/self_hosted/v1/distribution_credentials/client.py">delete</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Deletes a set of distribution credentials for the specified project
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from deepgram import DeepgramClient

client = DeepgramClient(
    api_key="YOUR_API_KEY",
)
client.self_hosted.v1.distribution_credentials.delete(
    project_id="123456-7890-1234-5678-901234",
    distribution_credentials_id="8b36cfd0-472f-4a21-833f-2d6343c3a2f3",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**project_id:** `str` — The unique identifier of the project
    
</dd>
</dl>

<dl>
<dd>

**distribution_credentials_id:** `str` — The UUID of the distribution credentials
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Speak V1 Audio
<details><summary><code>client.speak.v1.audio.<a href="src/deepgram/speak/v1/audio/client.py">generate</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Convert text into natural-sounding speech using Deepgram's TTS REST API
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from deepgram import DeepgramClient

client = DeepgramClient(
    api_key="YOUR_API_KEY",
)
client.speak.v1.audio.generate(
    text="text",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**text:** `str` — The text content to be converted to speech
    
</dd>
</dl>

<dl>
<dd>

**callback:** `typing.Optional[str]` — URL to which we'll make the callback request
    
</dd>
</dl>

<dl>
<dd>

**callback_method:** `typing.Optional[AudioGenerateRequestCallbackMethod]` — HTTP method by which the callback request will be made
    
</dd>
</dl>

<dl>
<dd>

**mip_opt_out:** `typing.Optional[bool]` — Opts out requests from the Deepgram Model Improvement Program. Refer to our Docs for pricing impacts before setting this to true. https://dpgr.am/deepgram-mip
    
</dd>
</dl>

<dl>
<dd>

**tag:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — Label your requests for the purpose of identification during usage reporting
    
</dd>
</dl>

<dl>
<dd>

**bit_rate:** `typing.Optional[float]` — The bitrate of the audio in bits per second. Choose from predefined ranges or specific values based on the encoding type.
    
</dd>
</dl>

<dl>
<dd>

**container:** `typing.Optional[AudioGenerateRequestContainer]` — Container specifies the file format wrapper for the output audio. The available options depend on the encoding type.
    
</dd>
</dl>

<dl>
<dd>

**encoding:** `typing.Optional[AudioGenerateRequestEncoding]` — Encoding allows you to specify the expected encoding of your audio output
    
</dd>
</dl>

<dl>
<dd>

**model:** `typing.Optional[AudioGenerateRequestModel]` — AI model used to process submitted text
    
</dd>
</dl>

<dl>
<dd>

**sample_rate:** `typing.Optional[float]` — Sample Rate specifies the sample rate for the output audio. Based on the encoding, different sample rates are supported. For some encodings, the sample rate is not configurable
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration. You can pass in configuration such as `chunk_size`, and more to customize the request and response.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

