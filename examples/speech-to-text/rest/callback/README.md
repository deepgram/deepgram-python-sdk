# Callback Example

This example shows how to use the [Callback](https://developers.deepgram.com/docs/callback) functionality on the Prerecorded API.

> **_NOTE:_** To use this example, the `endpoint` component must run somewhere with a public-facing IP address. You cannot run this example locally behind your typical firewall.

## Configuration

This example consists of two components:
- `endpoint`: which is an example of what a callback endpoint would look like. Reminder: this requires running with a public-facing IP address
- `callback`: which is just a Deepgram client posts a PreRecorded transcription request using a local audio file preamble.wav (or using an audio file at a hosted URL, like [https://static.deepgram.com/examples/Bueller-Life-moves-pretty-fast.wav](https://static.deepgram.com/examples/Bueller-Life-moves-pretty-fast.wav).

The `callback` component requires the Deepgram API Key environment variable to be configured to run.

```sh
export DEEPGRAM_API_KEY=YOUR-APP-KEY-HERE
```

### Prerequisites: Public-facing Endpoint

This example requires that the Deepgram platform be able to reach your `endpoint` which means the IP address must be publically hosted. This could be an EC2 instance on AWS, an instance on GCP, etc. Another option is using [ngrok](https://ngrok.com/).

`ngrok` brief overview: run ngrok http 8080 which opens up the local host port 8080, and gives a public URL https://e00a-42-156-98-177.ngrok-free.app/ (for example). Then in another terminal, run nc -l 8080 to listen on port 8080 for incoming messages. The `CALL_BACK_URL` should then be set to `https://e00a-42-156-98-177.ngrok-free.app`.

## Installation

Run the `endpoint` application using an SSL certificate to a system on the public-facing internet.

On the `callback` project, modify the IP address constant in the code with the public-facing IP address of your EC2, GCP, etc instance.

```Python
CALL_BACK_URL = (
    "https://127.0.0.1:8000"  # TODO: MUST REPLACE WITH YOUR OWN CALLBACK ENDPOINT
)
```

Then run the `callback` application. This can be done from your local laptop.
