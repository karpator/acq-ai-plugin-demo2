"""
Czech Republic specific greeting implementation.
"""

from typing import Any

from shared.core.registry import plugin
from shared.services.greeting import Greet


@plugin(Greet)
class CzechGreet(Greet):
    """Czech-specific greeting implementation."""

    def say_hello(self, name: str) -> str:
        """Say hello in Czech."""
        return f"Ahoj, {name}!"

    def say_goodbye(self, name: str) -> str:
        """Say goodbye in Czech."""
        return f"Na shledanou, {name}!"

    def get_greeting_info(self) -> dict[str, Any]:
        """Get information about this Czech implementation."""
        return {
            "class": self.__class__.__name__,
            "module": self.__class__.__module__,
            "type": "czech_plugin",
            "country": "cz",
            "language": "Czech",
        }
