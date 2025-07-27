from shared.core.registry import plugin
from shared.services.name import Name


@plugin(Name)
class CzechName(Name):
    """Czech-specific name implementation."""

    @staticmethod
    def get() -> str:
        """Get the name of the person in Czech."""
        return "České Jméno"
