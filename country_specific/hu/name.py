from shared.core.registry import plugin
from shared.services.name import Name


@plugin(Name)
class HungarianName(Name):
    """Hungarian-specific name implementation."""

    @staticmethod
    def get() -> str:
        """Get the name of the person in Hungarian."""
        return "Magyar Név"
