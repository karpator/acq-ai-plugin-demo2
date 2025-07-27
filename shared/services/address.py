from shared.core.registry import pluggable


@pluggable
class Address:
    """
    Base address class that can be overridden by country-specific plugins.
    """

    def __init__(self, street: str, city: str, postal_code: str):
        """Initialize the address service."""
        self.default_country = "US"
        self.separator = ", "
        self.street = street
        self.city = city
        self.postal_code = postal_code

    def format_address(self) -> str:
        """
        Format an address. Must be implemented by all plugins.

        Args:
            street: Street address
            city: City name
            postal_code: Postal code

        Returns:
            Formatted address string
        """
        if not self._validate_postal_code(self.postal_code):
            raise ValueError(f"Invalid postal code: {self.postal_code}")
        return f"{self.street}{self.separator}{self.city}{self.separator}{self.postal_code}"

    def get_country(self) -> str:
        """
        Get the default country for this address service.

        Returns:
            Country code
        """
        return self.default_country

    def get_address_info(self) -> dict[str, str]:
        """
        Get address information as a dictionary.

        Returns:
            Dictionary with address details
        """
        return {
            "class": self.__class__.__name__,
            "country": self.get_country(),
            "separator": self.separator,
        }

    def _validate_postal_code(self, postal_code: str) -> bool:
        """
        Basic postal code validation.

        Args:
            postal_code: Postal code to validate

        Returns:
            True if valid, False otherwise
        """
        return len(postal_code.strip()) > 0
