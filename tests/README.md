# Frontend Test Files

This folder contains the frontend test files for the WaterSafe Vue.js application.

## Test Files

- **HomeView.test.js** - Tests for the main home page component
- **MaternalInfantHealth.test.js** - Tests for the maternal and infant health features
- **Navigation.test.js** - Tests for the navigation component
- **WaterHealthInfo.test.js** - Tests for the water health information system
- **setup.js** - Test environment setup and configuration

## Running Tests

```bash
# Run all tests
npm test

# Run tests with coverage
npm run test:coverage

# Run tests in watch mode
npm run test:ui
```

## Test Configuration

- **Framework**: Vitest with Vue Test Utils
- **Environment**: JSDOM for browser simulation
- **Coverage**: Comprehensive coverage reporting
- **Mocking**: Component and dependency mocking

For detailed testing documentation, see `testing-docs/README.md`.