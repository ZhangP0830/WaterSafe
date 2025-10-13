# Backend Test Files

This folder contains the backend test files for the WaterSafe FastAPI application.

## Test Files

- **test_main.py** - Tests for the main FastAPI application
- **test_water_quality_prediction.py** - Tests for water quality prediction API
- **test_guidance_api.py** - Tests for guidance and checklist generation API
- **test_database.py** - Tests for database operations
- **test_integration.py** - Integration tests for end-to-end workflows
- **conftest.py** - Test configuration and fixtures

## Running Tests

```bash
# Run all tests
python run_backend_tests.py

# Run tests with coverage
python -m pytest tests/ --cov=. --cov-report=html

# Run specific test file
python -m pytest tests/test_main.py -v
```

## Test Configuration

- **Framework**: pytest with async support
- **Coverage**: Comprehensive coverage reporting
- **Mocking**: Database and external API mocking
- **Fixtures**: Reusable test data and configuration

For detailed testing documentation, see `testing-docs/README.md`.