# [Private Beta] SageMakerRuntime BiDi API Contract

### 1. HTTP/2 Request Syntax

```
POST https://runtime.sagemaker.us-east-2.amazonaws.com:8443/endpoints/<EndpointName>/invocations-bidirectional-stream

[Optional] X-Amzn-SageMaker-Target-Variant: <TargetVariant>
[Optional] X-Amzn-SageMaker-Model-Invocation-Path: <ModelInvocationPath>
[Optional] X-Amzn-SageMaker-Model-Query-String: <ModelQueryString>
{
  "PayloadPart": {
    "Bytes": <Blob>,
    "DataType": <String: UTF8 | BINARY>,
    "CompletionState": <String: PARTIAL | COMPLETE>,
    "P": <String>
  }
}
```

More detailed explanation **(you can skip this part if you are already familiar with SageMaker publi APIs):**

- [Optional] TargetVariant:
  - Specify the production variant to send the inference request to when invoking an endpoint that is running two or more variants. Note that this parameter overrides the default behavior for the endpoint, which is to distribute the invocation traffic based on the variant weights.
  - Length Constraints: Maximum length of 63.
  - Pattern: **`^[a-zA-Z0-9](-*[a-zA-Z0-9])*`**
- [Optional] ModelInvocationPath:
  - SageMaker connections to model container using URL **`ws://local:8081/<ModelInvocationPath>`**. This parameter defaults to **`invoke-bidi-stream`** if not specified.
  - Length Constraints: Maximum length of 100.
  - Pattern: **`^[A-Za-z0-9\-._]+(?:/[A-Za-z0-9\-._]+)*$`**
- [Optional] ModelQueryString:
  - If specified, SageMaker appends it to the URL when connecting to model containers: **`ws://local:8081/<ModelInvocationPath>?<ModelQueryString>`**.
  - Length Constraints: Maximum length of 2048.
  - Pattern: **`^[a-zA-Z0-9][A-Za-z0-9_-]*=(?:[A-Za-z0-9._~\-]|%[0-9A-Fa-f]{2})+(?:&[a-zA-Z0-9][A-Za-z0-9_-]*=(?:[A-Za-z0-9._~\-]|%[0-9A-Fa-f]{2})+)*$`**
- [Required] RequestStream (the following data is sent in JSON format by the client to the service):
  - PayloadPart: A wrapper object of input payload. A request stream consists of one or more pieces of PayloadParts. This object has the following fields:
    - [Required] Bytes:
      - Base64 encoded binary chunk.
    - [Optional] DataType:
      - Regex Pattern: **`^(UTF8)$|^(BINARY)$`**
      - If this field is null, SageMaker defaults the value to **`BINARY`**.
      - If **`DataType = UTF8`**, the binary chunk contains the raw bytes of a UTF-8 encoded string.
    - [Optional] CompletionStatus:
      - Regex Pattern: **`^(PARTIAL)$|^(COMPLETE)$`**
      - If this field is null, SageMaker defaults the value to **`COMPLETE`**.
      - A binary chunk may be fragmented across multiple PayloadParts. If **`CompletionStatus = PARTIAL`**, the current PayloadPart is incomplete and shall be aggregated with subsequent PayloadPart until one with **`CompletionStatus = COMPLETE`** is received.
      - An un-fragmented binary chunk always has **`CompletionStatus = COMPLETE`**.
      - Note that SageMaker does not aggregate PayloadParts on customers’ behalf, the fragments are passed to model containers as-is.
    - [Optional] P:
      - Padding string defending against﻿ token length side channel attack﻿ .

### 2. HTTP/2 Response Syntax

Response event stream is a union of (by union, we are saying an event in the output stream can be one (and only one) of the followings):

- ResponsePayload is passed all the way from model container to customer, **_which SageMaker never inspects into_**;
- InternalStreamFailure: mid stream server-side fault (similar to 500 error code, but not the same);
- ModelStreamError: mid stream errors originated from inside the Model Container (similar to 400 error code, but not the same).

```
HTTP/2 200
x-Amzn-Invoked-Production-Variant: <InvokedProductionVariant>

{
  "PayloadPart": {
    "Bytes": <Blob>,
    "DataType": <String: UTF8 | BINARY>,
    "CompletionState": <String: PARTIAL | COMPLETE>,
    "P": <String>
  },
  "ModelStreamError": {
    "ErrorCode": <String>,
    "Message": <String>
  },
  "InternalStreamFailure": {
    "Message": <String>
  }
}
```

More detailed explanation **(you can skip this part if you are already familiar with SageMaker publi APIs):**

- InvokedProductionVariant:
  - Identifies the production variant that was invoked.
  - Length Constraints: Maximum length of 1024.
  - Pattern: `\p{ASCII}*`
- ResponseStream contains three types of events: PayloadPart, ModelStreamError or InternalStreamFailure. The following data is returned in JSON format by the service:
  - PayloadPart: A wrapper object of output payload. A response stream consists of one or more pieces of PayloadParts. This object has the following fields:
    - [Required] Bytes:
      - Base64 encoded binary chunk.
    - [Optional] DataType:
      - Regex Pattern: **`^(UTF8)$|^(BINARY)$`**
      - If this field is null, SageMaker defaults the value to **`BINARY`**.
      - If **`DataType = UTF8`**, the binary chunk contains the raw bytes of a UTF-8 encoded string.
    - [Optional] CompletionStatus:
      - Regex Pattern: **`^(PARTIAL)$|^(COMPLETE)$`**
      - If this field is null, SageMaker defaults the value to **`COMPLETE`**.
      - A binary chunk may be fragmented across multiple PayloadParts. If **`CompletionStatus = PARTIAL`**, the current PayloadPart is incomplete and shall be aggregated with subsequent PayloadPart until one with **`CompletionStatus = COMPLETE`** is received.
      - An unfragmented binary chunk always has **`CompletionStatus = COMPLETE`**.
      - Note that SageMaker does not aggregate PayloadParts on customers’ behalf, the fragments are passed from model container to clients as-is.
    - [Optional] P:
      - Padding string defending against﻿ token length side channel attack﻿.
  - ModelStreamError: An error originated from the model container while streaming the response body.
  - InternalStreamFailure: A fault originated from SageMaker platform while streaming the response body . The stream processing failed because of an unknown error, exception or failure. Try your request again.
