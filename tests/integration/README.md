# Integration Tests

This directory contains integration tests that verify the Deepgram Python Core SDK works correctly against the production API.

## Structure

The integration tests mirror the structure of the `examples/` directory to ensure comprehensive coverage of all SDK functionality:

```
tests/integration/
├── listen/
│   └── media/
│       └── transcribe_url/
│           ├── test_main.py      # Sync version tests
│           └── test_async.py     # Async version tests
└── README.md
```

## Running Integration Tests

### Prerequisites

1. **API Key**: Set the `DEEPGRAM_API_KEY` environment variable:

   ```bash
   export DEEPGRAM_API_KEY=your_api_key_here
   ```

2. **Dependencies**: Install the development dependencies:
   ```bash
   poetry install
   ```

### Running Tests

To run all integration tests:

```bash
poetry run pytest tests/integration/
```

To run specific integration test modules:

```bash
# Run only sync transcribe_url tests
poetry run pytest tests/integration/listen/media/transcribe_url/test_main.py

# Run only async transcribe_url tests
poetry run pytest tests/integration/listen/media/transcribe_url/test_async.py
```

To run with verbose output:

```bash
poetry run pytest tests/integration/ -v
```

### Test Skipping

Tests will automatically skip if the `DEEPGRAM_API_KEY` environment variable is not set, preventing failures in environments where API access is not available.

## Test Coverage

Each integration test module covers:

1. **Basic functionality** - Verifying the core API call works
2. **Response structure** - Ensuring the response matches expected types
3. **Options and parameters** - Testing various API parameters
4. **Error handling** - Testing invalid inputs and error conditions
5. **Model variations** - Testing different models when applicable

## Adding New Integration Tests

When adding new integration tests:

1. **Mirror the examples structure** - Create the same directory hierarchy as in `examples/`
2. **Test both sync and async** - Create separate test files for synchronous and asynchronous versions
3. **Use real API calls** - These are integration tests, so they should make actual API requests
4. **Handle API keys gracefully** - Always check for API key availability and skip if not present
5. **Test realistic scenarios** - Use the same test data and parameters as the examples
6. **Document the tests** - Include docstrings explaining what each test verifies

## Code Generation Exclusion

The `tests/integration/` directory is excluded from code generation via the `.fernignore` file, ensuring these tests won't be overwritten when the SDK is regenerated.

## CI/CD Integration

These integration tests are automatically discovered and run by the existing pytest configuration in `pyproject.toml`. The CI/CD pipeline in `.github/workflows/ci.yml` will run these tests along with the existing unit tests.

**Note**: For CI/CD environments, ensure the `DEEPGRAM_API_KEY` secret is properly configured if you want integration tests to run in automated builds.
