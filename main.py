"""
Main application entry point with country-specific plugin loading.
"""

import logging
import sys
from typing import Optional

from shared.core.country_loader import (
    CountryPluginLoader,
    load_country_specific_plugins,
)
from shared.core.registry import PluginRegistry
from shared.services.greeting import Greet


def setup_logging():
    """Configure logging for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(name)s - %(levelname)s - %(message)s",
    )


def main():
    """Main application function."""
    setup_logging()
    logger = logging.getLogger(__name__)

    # Show available countries
    loader = CountryPluginLoader()
    available_countries = loader.get_available_countries()
    logger.info(f"Available countries: {available_countries}")

    # Get country code from command line argument if provided
    country_code: Optional[str] = None
    if len(sys.argv) > 1:
        country_code = sys.argv[1].lower()
        logger.info(f"Country code from command line: {country_code}")

    # Load country-specific plugins
    if not load_country_specific_plugins(country_code):
        logger.error("Failed to load country-specific plugins")
        sys.exit(1)

    # Show what was loaded
    loaded_countries = loader.get_loaded_countries()
    logger.info(f"Loaded countries: {loaded_countries}")

    # Get registry info
    registry = PluginRegistry()
    pluggable_classes = registry.get_pluggable_classes()
    logger.info(f"Pluggable classes: {pluggable_classes}")

    # Test the greeting service
    logger.info("Testing greeting service...")
    
    try:
        # Create greeting instance (should use country-specific plugin)
        greeter = Greet()
        
        # Get info about the implementation
        info = greeter.get_greeting_info()
        logger.info(f"Using greeting implementation: {info}")
        
        # Test greetings
        hello_msg = greeter.say_hello("World")
        goodbye_msg = greeter.say_goodbye("World")
        
        print(f"Hello: {hello_msg}")
        print(f"Goodbye: {goodbye_msg}")
        print(f"Implementation: {info['class']} ({info.get('country', 'unknown')})")
        
    except Exception as e:
        logger.error(f"Error during testing: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
