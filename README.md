# Plugin2 - Country-Specific Plugin System

A demonstration of a country-specific plugin system that selectively loads plugins based on configuration to avoid registry conflicts.

## Features

- **Selective Plugin Loading**: Only loads plugins for the specified country
- **Multiple Configuration Methods**: Command line, environment variable, or config file
- **Comprehensive Logging**: Detailed logging to track plugin loading and execution
- **Entry Points Integration**: Uses setuptools entry points for plugin discovery
- **uv Package Manager Support**: Built and tested with uv

## Available Countries

- `cz` - Czech Republic (Ahoj/Na shledanou)
- `hu` - Hungary (Szia/Viszlát)

## Installation

Using uv (recommended):

```bash
# Create virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode
uv pip install -e .
```

## Usage

### Method 1: Command Line Argument

```bash
python main.py cz    # Load Czech plugins
python main.py hu    # Load Hungarian plugins
```

### Method 2: Environment Variable

```bash
export PLUGIN2_COUNTRY=cz
python main.py

# Or inline:
PLUGIN2_COUNTRY=hu python main.py
```

### Method 3: Configuration File

Create a `country_config.txt` file with the country code:

```bash
echo "cz" > country_config.txt
python main.py
```

### Priority Order

1. Command line argument (highest priority)
2. Environment variable (`PLUGIN2_COUNTRY`)
3. Configuration file (`country_config.txt`)

## Testing

Run the comprehensive test suite:

```bash
python test_country_loading.py
```

This tests:
- Czech Republic plugin loading
- Hungarian plugin loading
- Invalid country code handling
- Environment variable loading
- Configuration file loading

## Example Output

```
2025-07-27 21:44:04,978 - __main__ - INFO - Starting plugin2 application
2025-07-27 27 21:44:04,990 - __main__ - INFO - Available countries: ['cz', 'hu']
2025-07-27 21:44:04,990 - __main__ - INFO - Country code from command line: cz
2025-07-27 21:44:04,990 - shared.core.country_loader - INFO - Loading plugins for country: cz
2025-07-27 21:44:04,991 - shared.core.registry - INFO - Registered plugin CzechGreet for Greet
2025-07-27 21:44:04,991 - shared.core.country_loader - INFO - Successfully loaded cz plugins from country_specific.cz.greeting

Greeting Results:
Hello: Ahoj, World!
Goodbye: Na shledanou, World!
Implementation: CzechGreet (cz)
```

## Architecture

### Key Components

1. **CountryPluginLoader** (`shared/core/country_loader.py`): Manages selective plugin loading
2. **PluginRegistry** (`shared/core/registry.py`): Centralized plugin registration system  
3. **Entry Points** (`pyproject.toml`): Defines available country plugins
4. **Country-Specific Modules**: Implement country-specific greeting logic

### How It Works

1. The application discovers available countries from setuptools entry points
2. Based on configuration, it loads only the specified country's plugin module
3. The plugin system registers the country-specific implementation
4. When creating instances, the registry returns the country-specific plugin instead of the base class

### Benefits

- **No Registry Conflicts**: Only one country's plugins are loaded at a time
- **Clean Separation**: Each country's code is isolated
- **Extensible**: Easy to add new countries by adding entry points
- **Testable**: Comprehensive test coverage with multiple configuration methods

## Adding New Countries

1. Create a new directory under `country_specific/` (e.g., `country_specific/de/`)
2. Implement the greeting plugin following the existing pattern
3. Add an entry point in `pyproject.toml`:
   ```toml
   [project.entry-points."plugin2.countries"]
   de = "country_specific.de.greeting"
   ```
4. Reinstall the package: `uv pip install -e .`

## Development

The project uses:
- **uv** for package management
- **setuptools** for building and entry points
- **Python 3.10+** for type hints and modern features
- **Comprehensive logging** for debugging and monitoring
