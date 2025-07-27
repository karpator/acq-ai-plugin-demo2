"""
Standalone entry point for the shared module.

This demonstrates how the shared module can run independently
without any country-specific plugins.
"""

import logging

from core.registry import PluginRegistry
from services.greeting import Greet

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


class DefaultGreet(Greet):
    """Default implementation of the Greet class for standalone use."""

    def say_hello(self, name: str) -> str:
        """Basic hello implementation."""
        return f"Hello, {name}!"

    def get_greeting_info(self) -> dict[str, str]:
        """Override to indicate this is the default implementation."""
        info = super().get_greeting_info()
        info["type"] = "default"
        return info


def main():
    """Main function for standalone shared module."""
    logger.info("Starting shared module in standalone mode")

    registry = PluginRegistry()
    logger.info(f"Pluggable classes: {registry.get_pluggable_classes()}")

    # For standalone mode, we need to manually create the default implementation
    # since no plugins are loaded
    greeter = DefaultGreet()

    print("=== Shared Module Demo ===")
    print(f"Using: {greeter.__class__.__name__}")
    print(f"Info: {greeter.get_greeting_info()}")
    print(f"Hello: {greeter.say_hello('World')}")
    print(f"Goodbye: {greeter.say_goodbye('World')}")

    logger.info("Shared module demo completed")


if __name__ == "__main__":
    main()
