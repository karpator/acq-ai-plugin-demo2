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
from shared.services.address import Address
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

    # # Show what was loaded
    # loaded_countries = loader.get_loaded_countries()
    # logger.info(f"Loaded countries: {loaded_countries}")

    # Get registry info
    registry = PluginRegistry()
    pluggable_classes = registry.get_pluggable_classes()
    logger.info(f"Pluggable classes: {pluggable_classes}")

    print("\nGreetings Testing:")
    print("-" * 20)
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
        hello_msg2 = greeter.say_hello2()
        goodbye_msg = greeter.say_goodbye("World")
        message_end = Greet.message_end()


        print(f"Hello: {hello_msg}")
        print(f"Hello Version 2: {hello_msg2}")
        print(f"Goodbye: {goodbye_msg}")
        print(f"Implementation: {info['class']} ({info.get('country', 'unknown')})")
        print(f"Message end: '{message_end}'")
        print()

        # For Hungarian addresses, use 4-digit postal codes
        # For default (US) addresses, any non-empty string is valid
        if country_code == "hu":
            valid_postal_code = "8200"  # Valid 4-digit Hungarian postal code
            invalid_postal_code = "10 0"  # Invalid (contains space and not 4 digits)
            alternative_invalid = "123"  # Invalid (only 3 digits)
        else:
            valid_postal_code = "12345"  # Valid for default US format
            invalid_postal_code = ""  # Invalid (empty string)
            alternative_invalid = "   "  # Invalid (only spaces)

        print("\nAddress Testing:")
        print("-" * 20)

        # Test with valid postal code
        try:
            address_valid = Address("123 Main Street", "Budapest", valid_postal_code)
            address_info = address_valid.get_address_info()
            logger.info(f"Using address implementation: {address_info}")

            formatted_address = address_valid.format_address()
            print(f"✓ Valid address: {formatted_address}")
            print(
                f"  Implementation: {address_info['class']} ({address_info.get('country', 'unknown')})"
            )
            print(f"  Separator: '{address_info['separator']}'")
        except Exception as e:
            logger.error(f"Error with valid postal code '{valid_postal_code}': {e}")
            print(f"✗ Error with valid postal code: {e}")

        # Test with invalid postal code
        try:
            address_invalid = Address("456 Oak Avenue", "Vienna", invalid_postal_code)
            formatted_address_invalid = address_invalid.format_address()
            print(
                f"✗ Invalid address (should not reach here): {formatted_address_invalid}"
            )
        except ValueError as e:
            logger.info(
                f"Correctly caught invalid postal code '{invalid_postal_code}': {e}"
            )
            print(f"✓ Invalid postal code test passed: '{invalid_postal_code}' -> {e}")
        except Exception as e:
            logger.error(
                f"Unexpected error with invalid postal code '{invalid_postal_code}': {e}"
            )
            print(f"✗ Unexpected error: {e}")

        # Test with alternative invalid postal code (for completeness)
        try:
            address_invalid2 = Address("789 Pine Street", "Prague", alternative_invalid)
            formatted_address_invalid2 = address_invalid2.format_address()
            print(
                f"✗ Alternative invalid address (should not reach here): {formatted_address_invalid2}"
            )
        except ValueError as e:
            logger.info(
                f"Correctly caught alternative invalid postal code '{alternative_invalid}': {e}"
            )
            print(
                f"✓ Alternative invalid postal code test passed: '{alternative_invalid}' -> {e}"
            )
        except Exception as e:
            logger.error(
                f"Unexpected error with alternative invalid postal code '{alternative_invalid}': {e}"
            )
            print(f"✗ Unexpected error with alternative invalid: {e}")

    except Exception as e:
        logger.error(f"Error during testing: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
