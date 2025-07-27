"""
Plugin registry and decorators for the plugin system.

This module provides the core functionality for:
- Registering and discovering plugins
- Decorators for marking classes as pluggable and plugins
"""

import logging
from typing import Any, Callable, Dict, Optional, TypeVar

# Configure logging
logger = logging.getLogger(__name__)


def override_required(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorator to mark a method as required for plugin implementations.

    This decorator replaces abstractmethod and raises a PluginRequiredMethodError
    if a plugin doesn't implement the required method.

    Args:
        func: The method to mark as required

    Returns:
        The decorated method

    Raises:
        PluginRequiredMethodError: When called on a method that hasn't been overridden
    """

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # Get the class that defined this method
        calling_class = args[0].__class__
        method_name = func.__name__

        # Check if this method has been overridden in the calling class
        # by comparing the actual implementation
        current_method = getattr(calling_class, method_name)

        # If current_method is the same as our wrapper, it means it hasn't been overridden
        if hasattr(current_method, "__override_required__"):
            raise PluginRequiredMethodError(
                f"Plugin '{calling_class.__name__}' must implement the required method '{method_name}'. "
                f"This method is marked as @override_required and cannot use the base implementation."
            )

        # If overridden, call the actual implementation
        return current_method(*args, **kwargs) # type: ignore[return-value]

    # Mark the function as override required for introspection
    setattr(wrapper, "__override_required__", True)
    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__

    return wrapper


class PluginRequiredMethodError(Exception):
    """Raised when a plugin doesn't implement a required method."""

    pass


class PluginValidationError(Exception):
    """Raised when plugin validation fails."""

    pass


class PluginRegistrationError(Exception):
    """Raised when plugin registration fails."""

    pass


class PluginRegistry:
    """
    Centralized registry for managing plugin overrides.

    This is a singleton class that manages all plugin registrations,
    lookups, and validations across the application.
    """

    _instance: Optional["PluginRegistry"] = None
    _initialized: bool = False

    def __new__(cls) -> "PluginRegistry":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self._plugins: Dict[str, type] = {}  # {class_name: plugin_class}
            self._pluggable_classes: Dict[str, type] = {}  # {class_name: base_class}
            self._class_metadata: Dict[
                str, Dict[str, Any]
            ] = {}  # {class_name: metadata}
            PluginRegistry._initialized = True
            logger.info("PluginRegistry initialized")

    def register_pluggable(
        self, cls: type, metadata: Optional[Dict[str, Any]] = None
    ) -> type:
        """
        Register a class as pluggable.

        Args:
            cls: The base class to mark as pluggable
            metadata: Optional metadata about the class

        Returns:
            The original class (for use as decorator)
        """
        class_name = cls.__name__
        self._pluggable_classes[class_name] = cls
        self._class_metadata[class_name] = metadata or {}

        logger.info(f"Registered pluggable class: {class_name}")
        return cls

    def register_plugin(self, target_class: type, plugin_class: type) -> None:
        """
        Register a plugin class for a target class.

        Args:
            target_class: The base class being overridden
            plugin_class: The plugin implementation

        Raises:
            PluginValidationError: If validation fails
            PluginRegistrationError: If registration fails
        """
        target_name = target_class.__name__

        # Validate that target class is pluggable
        if target_name not in self._pluggable_classes:
            raise PluginRegistrationError(
                f"Target class {target_name} is not registered as pluggable"
            )

        # Validate inheritance
        if not issubclass(plugin_class, target_class):
            raise PluginValidationError(
                f"Plugin class {plugin_class.__name__} must inherit from {target_name}"
            )

        # Register the plugin
        if target_name in self._plugins:
            logger.warning(f"Overriding existing plugin for {target_name}")

        self._plugins[target_name] = plugin_class
        logger.info(f"Registered plugin {plugin_class.__name__} for {target_name}")

    def get_plugin_class(self, base_class: type) -> type:
        """
        Get the plugin class for a base class.

        Args:
            base_class: The base class to find a plugin for

        Returns:
            The plugin class if found, otherwise the base class
        """
        class_name = base_class.__name__
        plugin_class = self._plugins.get(class_name)

        if plugin_class:
            logger.debug(f"Using plugin {plugin_class.__name__} for {class_name}")
            return plugin_class
        else:
            logger.debug(f"No plugin found for {class_name}, using base class")
            return base_class

    def get_pluggable_classes(self) -> list[str]:
        """Get list of all pluggable class names."""
        return list(self._pluggable_classes.keys())


T = TypeVar("T", bound=type)


class PluggableMeta(type):
    """
    Metaclass for pluggable classes that intercepts class-level attribute access
    to redirect static/class methods to plugin implementations.
    """
    
    def __getattribute__(cls, name: str) -> Any:
        # Skip special attributes and internal attributes to avoid recursion
        if (name.startswith('__') or name.startswith('_') or 
            name in ('mro', 'register', '__dict__', '__class__')):
            return super(PluggableMeta, cls).__getattribute__(name)
        
        # Only check for plugins if this is marked as pluggable
        # Use super() to avoid recursion when checking _is_pluggable
        try:
            is_pluggable = super(PluggableMeta, cls).__getattribute__('_is_pluggable')
        except AttributeError:
            is_pluggable = False
            
        if is_pluggable:
            # Get the registry
            registry = PluginRegistry()
            plugin_class = registry.get_plugin_class(cls)
            
            # If we have a plugin different from the base class
            # Compare by name since the classes might be different types
            if plugin_class.__name__ != cls.__name__ or plugin_class.__module__ != cls.__module__:
                # Check if the plugin has this attribute in its own __dict__ (not inherited)
                if name in plugin_class.__dict__:
                    plugin_attr = plugin_class.__dict__[name]
                    
                    # If it's a classmethod or staticmethod, use the descriptor protocol to get the bound version
                    if isinstance(plugin_attr, classmethod):
                        return plugin_attr.__get__(None, plugin_class)  # type: ignore[return-value]
                    elif isinstance(plugin_attr, staticmethod):
                        return plugin_attr.__get__(None, plugin_class)  # type: ignore[return-value]
        
        # For everything else, return the base attribute
        return super(PluggableMeta, cls).__getattribute__(name)


def pluggable(cls: T, *, metadata: Optional[Dict[str, Any]] = None) -> T:
    """
    Decorator to mark a class as pluggable.

    This decorator registers a class with the plugin registry as eligible
    for plugin overrides. The class __new__ method is modified to return
    plugin instances when available, and the metaclass handles static/class
    method redirection to plugins.

    Args:
        cls: The class to mark as pluggable
        metadata: Optional metadata about the class

    Returns:
        The decorated class with plugin support
    """

    def decorator(target_class: T) -> T:
        registry = PluginRegistry()
        registry.register_pluggable(target_class, metadata)

        # Create a new class with the PluggableMeta metaclass
        new_class = PluggableMeta(
            target_class.__name__,
            target_class.__bases__,
            dict(target_class.__dict__)
        )
        
        # Mark it as pluggable for the metaclass
        new_class._is_pluggable = True  # type: ignore[attr-defined]
        
        # Copy over the original class attributes
        for attr_name, attr_value in target_class.__dict__.items():
            if not attr_name.startswith('__') or attr_name in ('__module__', '__qualname__', '__doc__'):
                setattr(new_class, attr_name, attr_value)

        # Store original __new__ method
        original_new = target_class.__new__

        def plugin_aware_new(cls: type, *args: Any, **kwargs: Any) -> Any:
            # Get the appropriate plugin class
            plugin_class = registry.get_plugin_class(target_class)

            if plugin_class != target_class:
                # Create instance of plugin class directly
                # Use object.__new__ to avoid recursion
                instance = object.__new__(plugin_class)  # type: ignore[misc]
                return instance  # type: ignore[return-value]
            else:
                # Create instance of base class normally
                if original_new is object.__new__:
                    instance = object.__new__(cls)  # type: ignore[misc]
                else:
                    instance = original_new(cls, *args, **kwargs)  # type: ignore[misc]
                return instance  # type: ignore[return-value]

        new_class.__new__ = staticmethod(plugin_aware_new)  # type: ignore[method-assign]
        return new_class  # type: ignore[return-value]

    return decorator(cls)


def plugin(target_class: Any) -> Callable[[type], type]:
    """
    Decorator to register a class as a plugin for a target class.

    Args:
        target_class: The base class this plugin overrides

    Returns:
        Decorator function
    """

    def decorator(plugin_class: type) -> type:
        registry = PluginRegistry()
        # Register the plugin
        registry.register_plugin(target_class, plugin_class)
        return plugin_class

    return decorator
