# Live API (Real-Time) Example

This example uses the Microphone as input in order to detect conversation insights in what is being said. This example required additional components (for the microphone) to be installed in order for this example to function correctly. 

## Configuration

The SDK (and this example) needs to be initialized with your account's credentials `DEEPGRAM_API_KEY`, which are available in your [Deepgram Console][dg-console]. If you don't have a Deepgram account, you can [sign up here][dg-signup] for free.

You must add your `DEEPGRAM_API_KEY` to your list of environment variables. We use environment variables because they are easy to configure, support PaaS-style deployments, and work well in containerized environments like Docker and Kubernetes.

```bash
export DEEPGRAM_API_KEY=YOUR-APP-KEY-HERE
```

## Installation

The Live API (Real-Time) example makes use of a [microphone package](https://github.com/deepgram/deepgram-python-sdk/tree/main/deepgram/audio/microphone) contained within the repository. That package makes use of the [PortAudio library](http://www.portaudio.com/) which is a cross-platform open source audio library. If you are on Linux, you can install this library using whatever package manager is available (yum, apt, etc.) on your operating system. If you are on macOS, you can install this library using [brew](https://brew.sh/).

[dg-console]: https://console.deepgram.com/
[dg-signup]: https://console.deepgram.com/signup
