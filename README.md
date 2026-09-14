# Skyline

Terminal-based weather telemetry fetcher querying OpenWeatherMap REST endpoints for real-time localized diagnostics.

## Overview

Checking quick atmospheric metrics during terminal sessions often forces developers to open resource-heavy browsers or deal with unformatted payload outputs. `weather-fetch-cli` provides immediate, formatted weather metrics directly inside stdout without context-switching away from your active terminal environment. It handles authentication state, missing credentials, standard API status codes, and networking failures cleanly.

## How It Works

1. **Environment Initialization:** The utility invokes `dotenv.load_dotenv()` to source runtime secrets from local environment configurations (`.env`) without hardcoding API keys.
2. **Credential Guard:** The entry point checks for `OPENWEATHER_API_KEY` in `os.getenv()`. Missing keys trigger immediate termination via `sys.exit(1)` with formatted standard error messages.
3. **Execution Loop & Input Normalization:** An interactive REPL loop captures user string inputs, trims trailing whitespace, and filters explicit exit directives (`q`, `quit`, `exit`).
4. **Synchronous HTTP Engine:** Network calls use `requests.get()` directed at OpenWeatherMap's `data/2.5/weather` endpoint with metric parameter parameters and explicit 10-second timeout bounds.
5. **Status & Payload Handling:** HTTP status codes receive explicit conditional branching:
   - `404` maps to localized city search lookup failure.
   - `401` identifies invalid authentication tokens.
   - Unexpected HTTP ranges trigger `response.raise_for_status()`.
   - Network timeouts and connectivity disruptions map to specific standard exception blocks (`requests.exceptions.Timeout`, `requests.exceptions.RequestException`).
6. **Data Formatting:** Successful responses return decoded JSON dictionaries. The parsing module extracts nested key paths (`sys.country`, `main.temp`, `main.feels_like`, `main.humidity`, `weather[0].description`, `wind.speed`) and formats them into an aligned text layout.

## Key Features

* Interactive CLI execution loop allowing continuous metric lookups per session.
* Non-blocking configuration management using environment variables.
* Explicit handling for client error codes (`404 Not Found`, `401 Unauthorized`).
* Guaranteed socket termination via hardcoded request timeouts.
* Safe dictionary key extraction with fallbacks for optional metadata parameters.

## Tech Stack & Core Dependencies Breakdown

* **Python Target:** Python 3.10+
* **Standard Library:**
  * `os`: Interfacing with host environment variables.
  * `sys`: Managing process exit statuses and standard streams.
* **Third-Party Dependencies:**
  * `requests`: Simplified synchronous HTTP transport layer with built-in connection pooling and JSON decoding.
  * `python-dotenv`: Automated parsing of `.env` files into process environment dictionaries.

## Environment & Web-Based Quick Start

### GitHub Codespaces (Browser Only)

1. Click **Code** -> **Codespaces** -> **Create codespace on main**.
2. Once the container initializes, create a `.env` file in the project root:
   ```bash
   echo "OPENWEATHER_API_KEY=your_actual_api_key_here" > .env
   ```
3. Run the application:
   ```bash
   python main.py
   ```

## Local Setup via Virtual Environment
```text
# Clone and enter directory
git clone [https://github.com/your-username/weather-fetch-cli.git](https://github.com/your-username/weather-fetch-cli.git)
cd weather-fetch-cli

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install requests python-dotenv

# Set credentials and execute
echo "OPENWEATHER_API_KEY=your_actual_api_key_here" > .env
python main.py
```

## Repository Structure
```text
weather-fetch-cli/
├── .github/
│   └── workflows/
│       └── ci.yml          # Automated linting, formatting, type check & test pipeline
├── .env                    # Environment key storage (git-ignored)
├── .gitignore              # Explicit file exclusions for Python environments
├── main.py                 # Core CLI entry point, API caller, and formatting engine
└── README.md               # Architecture documentation and usage guide
```

## Roadmap

[ ] Type Stubbing & Strict Annotations: Expand internal structural payload typing using TypedDict models to replace untyped dict dictionary hints.

[ ] Async Network Migration: Refactor network operations to httpx or aiohttp to allow simultaneous queries across multiple geographic targets.

[ ] Custom Config Presets: Implement home directory configuration loading (~/.config/weather-fetch/config.json) to save default temperature units (Metric, Imperial, Standard) and default target locations.
