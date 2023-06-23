import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--api-key", "--key", "--token", "-K", "-T", action="store", help="Deepgram API Key"
    )

def pytest_configure(config):
    pytest.api_key = config.getoption('--api-key')
