"""
Hungarian specific greeting implementation.
"""

from typing import Any

from shared.core.registry import plugin
from shared.services.greeting import Greet


@plugin(Greet)
class HungarianGreet(Greet):
    """Hungarian-specific greeting implementation."""

    def say_hello(self, name: str) -> str:
        """Say hello in Hungarian."""
        return f"Szia, {name}!"

    def say_goodbye(self, name: str) -> str:
        """Say goodbye in Hungarian."""
        return f"Viszlát, {name}!"

    def get_greeting_info(self) -> dict[str, Any]:
        """Get information about this Hungarian implementation."""
        return {
            "class": self.__class__.__name__,
            "module": self.__class__.__module__,
            "type": "hungarian_plugin",
            "country": "hu",
            "language": "Hungarian",
        }
