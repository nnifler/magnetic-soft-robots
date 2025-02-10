"""Module for handling global keyboard shortcuts in a PySide6 application.

This module defines a class `GlobalShortcutFilter` to filter key events and trigger 
registered shortcuts. It also includes helper functions to adjust shortcuts based on 
the platform, locate widgets with specific methods, and set up global shortcuts.

Attributes:
    shortcuts_config (Dict[str, Dict[str, str]]): Configuration for shortcuts, 
        including key sequences and corresponding method names.
Classes:
    GlobalShortcutFilter: Filters events to catch and trigger registered shortcuts.
Functions:
    get_platform_specific_shortcuts(shortcuts: str) -> QKeySequence:
        Adjusts the shortcuts for the current platform.

    find_widget_with_method(widget: QWidget, method_name: str) -> QWidget:
        Recursively finds a child widget containing the specified method.

    setup_global_shortcuts(parent_widget: QObject):
        Sets up global shortcuts by installing an event filter on the parent widget.
"""
import platform
from typing import Dict, Callable
from PySide6.QtCore import QObject, QEvent, Qt
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import QWidget

shortcuts_config: Dict[str, Dict[str, str]] = {
    "open": {"key": "Ctrl+Shift+O", "method": "open_models_popup"},
    "import": {"key": "Ctrl+Shift+I", "method": "show_popup_import"},
}


class GlobalShortcutFilter(QObject):
    """Filters the events to catch the shortcuts."""

    def __init__(self, parent: QObject = None):
        """Initializes the shortcut filter

        Args: 
            parent (QObject, optional): The parent QObject. 
        """

        super().__init__(parent)
        self.shortcuts: Dict[str, Callable] = {}

    def register_shortcut(self, key_sequence: str, callback: Callable):
        """Registers a global shortcut and its callback. 

        Args:
            key_sequence (str): The key sequence for the shortcut. 
            callback (Callable): The function to be called when the shortcut is activated.
        """

        shortcut = QShortcut(QKeySequence(key_sequence), self.parent())
        shortcut.setContext(Qt.ApplicationShortcut)
        shortcut.activated.connect(callback)
        self.shortcuts[key_sequence] = callback

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        """Filters key press events to trigger shortcuts.

        Args:
            obj (QObject): The object receiving the events. 
            event (QEvent): The event to be filtered.

        Returns:
            bool: True if the event was handled. False otherwise.
        """

        if event.type() == QEvent.KeyPress:
            key_sequence = QKeySequence(event.key()).toString()
            if key_sequence in self.shortcuts:
                self.shortcuts[key_sequence]()
                return True
        return super().eventFilter(obj, event)


def get_platform_specific_shortcuts(shortcuts: str) -> QKeySequence:
    """Adjusts the shortcuts to be platform-specific. 

    Args:
        shortcuts (str): The shortcuts to adjust.

    Returns:
        QKeySequence: The adjusted shortcuts.
    """

    if platform.system() == "Darwin":
        return QKeySequence(shortcuts.replace("Ctrl", "Meta"))
    return QKeySequence(shortcuts)


def find_widget_with_method(widget: QWidget, method_name: str) -> QWidget:
    """Finds a child widget with the specified method.

    Args:
        widget (QWidget): The parent widget to search.
        method_name (str): The name of the method to find.

    Returns:
        QWidget: The child widget containing the method, or None if not found. 
    """

    if hasattr(widget, method_name):
        return widget

    for child in widget.findChildren(QWidget):
        result = find_widget_with_method(child, method_name)
        if result:
            return result
    return None


def setup_global_shortcuts(parent_widget: QObject):
    """Sets up global shortcuts by installing an event filter. 

    Args:
        parent_widget (QObject): The parent widget on which to install the shortcuts.
    """
    shortcut_filter = GlobalShortcutFilter(parent_widget)
    parent_widget.installEventFilter(shortcut_filter)

    for action_name, config in shortcuts_config.items():
        key_sequence = config["key"]
        method_name = config["method"]

        target_widget = find_widget_with_method(parent_widget, method_name)
        if target_widget and hasattr(target_widget, method_name):
            shortcut_filter.register_shortcut(
                key_sequence, getattr(target_widget, method_name)
            )
            print(
                f"Shortcut '{key_sequence}' connected to method '{method_name}'"
            )
        else:
            print(
                f"Warning: No method named '{method_name}' found in widget."
            )
