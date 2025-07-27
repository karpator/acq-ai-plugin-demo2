"""
Example greeting service for demonstration of the plugin system.
"""

from typing import Any

from shared.core.registry import pluggable, override_required


@pluggable
class Greet:
    """
    Base greeting class that can be overridden by country-specific plugins.
    """

    @override_required
    def say_hello(self, name: str) -> str:
        """
        Say hello to someone. Must be implemented by all plugins.

        Args:
            name: The name of the person to greet

        Returns:
            A greeting message
        """
        # This should never be called as plugins must override this method
        return f"Hello, {name}!"  # Default implementation that will trigger error if not overridden

    def say_goodbye(self, name: str) -> str:
        """
        Say goodbye to someone. Can be overridden by plugins.

        Args:
            name: The name of the person to say goodbye to

        Returns:
            A goodbye message
        """
        return f"Goodbye, {name}!"

    def get_greeting_info(self) -> dict[str, Any]:
        """
        Get information about this greeting implementation.

        Returns:
            Dictionary with implementation details
        """
        return {
            "class": self.__class__.__name__,
            "module": self.__class__.__module__,
            "type": "base",
        }
