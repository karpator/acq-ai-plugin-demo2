"""
Country-specific plugin loader that selectively loads plugins based on configuration.
"""

import importlib
import logging
import os
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class CountryPluginLoader:
    """
    Loads plugins only for a specified country to avoid registry conflicts.
    """

    def __init__(self):
        self._loaded_countries: List[str] = []
        self._available_countries = self._discover_available_countries()

    def _discover_available_countries(self) -> Dict[str, str]:
        """
        Discover available countries from entry points.

        Returns:
            Dictionary mapping country codes to module paths
        """
        import importlib.metadata

        # Get entry points for our plugin group
        entry_points = importlib.metadata.entry_points(group="plugin2.countries")
        countries: Dict[str, str] = {}

        for entry_point in entry_points:
            countries[entry_point.name] = entry_point.value
            logger.debug(
                f"Discovered country plugin: {entry_point.name} -> {entry_point.value}"
            )

        return countries


    def _load_all_modules_in_package(self, package_path: str) -> List[str]:
        """
        Discover and import all Python modules within a package.

        Args:
            package_path: The package path (e.g., 'country_specific.cz')

        Returns:
            List of imported module names
        """
        imported_modules: List[str] = []

        try:
            # Import the package first
            package = importlib.import_module(package_path)
            logger.debug(f"Imported package: {package_path}")

            # Get the package's file path
            if hasattr(package, "__path__"):
                package_dir = package.__path__[0]
                logger.debug(f"Package directory: {package_dir}")

                # Discover all .py files in the package directory
                for item in os.listdir(package_dir):
                    if item.endswith(".py") and item != "__init__.py":
                        module_name = item[:-3]  # Remove .py extension
                        full_module_path = f"{package_path}.{module_name}"

                        try:
                            importlib.import_module(full_module_path)
                            imported_modules.append(full_module_path)
                            logger.debug(f"Successfully imported: {full_module_path}")
                        except ImportError as e:
                            logger.warning(f"Failed to import {full_module_path}: {e}")
            else:
                logger.warning(f"Package {package_path} has no __path__ attribute")

        except ImportError as e:
            logger.error(f"Failed to import package {package_path}: {e}")

        return imported_modules

    def get_available_countries(self) -> List[str]:
        """Get list of available country codes."""
        return list(self._available_countries.keys())

    def load_country_plugins(self, country_code: str) -> bool:
        """
        Load plugins for a specific country.

        Args:
            country_code: The country code to load plugins for (e.g., 'cz', 'hu')

        Returns:
            True if plugins were loaded successfully, False otherwise
        """
        if country_code in self._loaded_countries:
            logger.info(f"Country {country_code} plugins already loaded")
            return True

        if country_code not in self._available_countries:
            logger.error(
                f"Country {country_code} not available. Available: {list(self._available_countries.keys())}"
            )
            return False

        module_path = self._available_countries[country_code]

        try:
            logger.info(f"Loading plugins for country: {country_code}")
            logger.debug(f"Importing package: {module_path}")

            # Import all modules in the country package
            imported_modules = self._load_all_modules_in_package(module_path)

            if imported_modules:
                self._loaded_countries.append(country_code)
                logger.info(
                    f"Successfully loaded {country_code} plugins from {len(imported_modules)} modules: {imported_modules}"
                )
                return True
            else:
                logger.warning(f"No modules found in package {module_path}")
                return False

        except ImportError as e:
            logger.error(
                f"Failed to load {country_code} plugins from {module_path}: {e}"
            )
            return False

    def get_loaded_countries(self) -> List[str]:
        """Get list of currently loaded country codes."""
        return self._loaded_countries.copy()

    def clear_loaded_countries(self):
        """Clear the list of loaded countries (for testing)."""
        self._loaded_countries.clear()


def get_country_from_config() -> Optional[str]:
    """
    Get the country code from environment variable or config file.

    Returns:
        Country code if found, None otherwise
    """
    # First check environment variable
    country = os.environ.get("PLUGIN2_COUNTRY")
    if country:
        logger.info(f"Country loaded from environment: {country}")
        return country.lower()

    # Check for config file
    config_file = "country_config.txt"
    if os.path.exists(config_file):
        try:
            with open(config_file, "r") as f:
                country = f.read().strip()
                if country:
                    logger.info(f"Country loaded from {config_file}: {country}")
                    return country.lower()
        except Exception as e:
            logger.warning(f"Failed to read {config_file}: {e}")

    logger.warning("No country configuration found")
    return None


def load_country_specific_plugins(country_code: Optional[str] = None) -> bool:
    """
    Load plugins for a specific country only.

    Args:
        country_code: Country code to load. If None, will try to get from config.

    Returns:
        True if plugins were loaded successfully, False otherwise
    """
    if country_code is None:
        country_code = get_country_from_config()

    if country_code is None:
        logger.error("No country code specified and none found in configuration")
        return False

    loader = CountryPluginLoader()
    return loader.load_country_plugins(country_code)
