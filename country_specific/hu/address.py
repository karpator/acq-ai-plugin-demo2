from shared.core.registry import plugin
from shared.services.address import Address


@plugin(Address)
class HungarianAddress(Address):
    """
    Hungarian address implementation.
    """

    def __init__(self, street: str, city: str, postal_code: str):
        """Initialize the Hungarian address service."""
        super().__init__(street, city, postal_code)
        self.default_country = "HU"
        self.separator = ": "

    def _validate_postal_code(self, postal_code: str) -> bool:
        return len(postal_code.strip()) == 4 and postal_code.isdigit()
