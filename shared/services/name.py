from shared.core.registry import pluggable


@pluggable
class Name:
    @staticmethod
    def get() -> str:
        """
        Get the name of the person.

        Returns:
            The name as a string.
        """
        return "Default Name"