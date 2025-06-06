# AWS Polly Speak Provider Example

This example demonstrates how to use AWS Polly as the speak provider for the Deepgram Voice Agent. It shows how to configure the agent to use AWS Polly's text-to-speech service for generating voice responses.

## Prerequisites

1. A Deepgram API key
2. AWS credentials (either IAM or STS)
3. Python 3.7 or higher
4. Required Python packages (install via `pip install -r requirements.txt`):

## Environment Variables

Set these credentials in your environment using the `export` command in the terminal.

```env
export DEEPGRAM_API_KEY=your_deepgram_api_key
export AWS_ACCESS_KEY_ID=your_aws_access_key_id
export AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
# Only needed if using STS credentials
export AWS_SESSION_TOKEN=your_aws_session_token
```

## Configuration Options

The example demonstrates two ways to use AWS Polly:

1. **IAM Credentials** (default):
   ```python
   options.agent.speak.provider.credentials = AWSPollyCredentials(
       type="IAM",
       region="us-west-2",
       access_key_id=os.getenv("AWS_ACCESS_KEY_ID", ""),
       secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "")
   )
   ```

2. **STS Credentials** (temporary credentials):
   ```python
   options.agent.speak.provider.credentials = AWSPollyCredentials(
       type="STS",
       region="us-west-2",
       access_key_id=os.getenv("AWS_ACCESS_KEY_ID", ""),
       secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", ""),
       session_token=os.getenv("AWS_SESSION_TOKEN", "")
   )
   ```

### AWS Polly Voice Options

You can customize the AWS Polly voice by modifying these settings:

```python
options.agent.speak.provider.voice = "Matthew"  # AWS Polly voice name
options.agent.speak.provider.language_code = "en-US"
options.agent.speak.provider.engine = "standard"  # or "neural" for neural voices
```

Available voices and their configurations can be found in the [AWS Polly documentation](https://docs.aws.amazon.com/polly/latest/dg/voicelist.html).

## Running the Example

1. Set up your environment variables in `.env`
2. Run the example:
   ```bash
   python main.py
   ```

## Notes

- The example uses MP3 encoding for audio output since that's what AWS Polly provides
- Make sure your AWS credentials have the necessary permissions to use AWS Polly
- The example includes speaker playback for testing the voice output
- The agent is configured to use Deepgram for speech-to-text and OpenAI for the language model

## Troubleshooting

1. If you get authentication errors, verify your AWS credentials are correct
2. If the voice doesn't sound right, check that you've selected a valid voice name and language code
3. If you get connection errors, ensure your Deepgram API key is valid
4. For STS credentials, make sure the session token is current and not expired