# EMTMadrid

[![PyPI](https://img.shields.io/pypi/v/emt-madrid)](https://pypi.org/project/emt-madrid/)
[![License](https://img.shields.io/pypi/l/emt-madrid)](https://github.com/fermartv/EMTMadrid/blob/main/LICENSE)
[![Python Version](https://img.shields.io/pypi/pyversions/emt-madrid)](https://pypi.org/project/emt-madrid/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

A modern, asynchronous Python wrapper for the Madrid EMT (Empresa Municipal de Transportes) API, providing easy access to real-time public transportation data in Madrid, Spain.

## Features

- Real-time bus arrival information
- Stop information and details
- Simple and intuitive interface
- Asynchronous API client using `aiohttp`
- Type hints for better development experience
- Modern Python 3.13+ codebase
- Comprehensive test suite
- Code quality tools pre-configured

## Installation

### Using pip

Install the package from PyPI:

```bash
pip install emt-madrid
```

### Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/fermartv/EMTMadrid.git
   cd EMTMadrid
   ```

2. Set up the development environment:
   ```bash
   make local-setup
   source .venv/bin/activate
   ```
   This will:
   - Install Python 3.13.2 using uv
   - Set up pre-commit hooks
   - Install all dependencies
   - Activate the virtual environment

## Usage

### Prerequisites

1. Python 3.13.2 or higher
2. An active EMT MobilityLabs account

### Authentication

To use the EMT MobilityLabs API, you need to register on their [official website](https://mobilitylabs.emtmadrid.es/). After registration:

1. Complete the email verification process
2. Note your login credentials (email and password)

### Basic Example

```python
import asyncio
from aiohttp import ClientSession
from emt_madrid import EMTClient

async def main():
    # Replace these with your actual credentials
    EMAIL = "your-email@example.com"
    PASSWORD = "your-password"
    STOP_ID = "72"  # Example stop ID

    async with ClientSession() as session:
        # Create EMT client
        emt_client = EMTClient(
            email=EMAIL,
            password=PASSWORD,
            stop_id=STOP_ID,
            session=session,
        )

        # Fetch stop information and arrivals
        arrivals = await emt_client.get_arrivals()
        
        # Get and display the data
        print("Stop Information:", arrivals)

if __name__ == "__main__":
    asyncio.run(main())
```

More examples can be found in the [example](example) directory. Run them with:

```bash
make run-example
```

### Available Methods

#### EMTClient
- `get_arrivals()`: Fetches and updates stop information
- `get_stop_info()`: Returns the stop information

## Development

### Project Structure

```
EMTMadrid/
├── emt_madrid/      # Main package source code
├── tests/           # Test files
├── example/         # Example scripts
├── pyproject.toml   # Project configuration
└── Makefile         # Development commands
```

### Available Commands

- `make install`: Install all dependencies
- `make update`: Update dependencies
- `make test`: Run tests
- `make test-coverage`: Run tests with coverage report
- `make check-typing`: Run static type checking
- `make check-lint`: Check code style
- `make check-format`: Check code formatting
- `make lint`: Fix code style issues
- `make format`: Format code
- `make pre-commit`: Run all checks and tests (used in CI)
- `make run-example`: Run the basic example

### Adding Dependencies

- For development dependencies:
  ```bash
  make add-dev-package package=package-name
  ```
  
- For production dependencies:
  ```bash
  make add-package package=package-name
  ```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Before submitting your PR, please make sure to:
- Run all tests with `make test`
- Ensure code style is consistent with `make lint` and `make format`
- Update the documentation if needed

## License

This project is licensed under the GPLv3 - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [EMT Madrid MobilityLabs](https://mobilitylabs.emtmadrid.es/) for providing the API
- [API Documentation](https://apidocs.emtmadrid.es/)
