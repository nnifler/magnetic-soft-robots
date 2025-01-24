from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
    QLabel, QSlider, QDoubleSpinBox, QComboBox, QPushButton,
    QGridLayout, QMessageBox, QLineEdit, QMenu, QListWidget, QFileDialog
)
from PySide6.QtCore import Qt, QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator, QKeySequence, QAction


class MSRHeaderWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.setFixedHeight(30)  # Maximal 1 cm Höhe
        header_layout = QHBoxLayout(self)
        header_layout.setContentsMargins(5, 0, 5, 0)
        header_layout.setSpacing(5)  # Minimaler Abstand zwischen Buttons

        msr_label = QLabel("MSR")
        msr_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        header_layout.addWidget(msr_label, alignment=Qt.AlignLeft)

        self.library_button = QPushButton("Library")
        self.library_button.clicked.connect(self.show_library_menu)
        header_layout.addStretch()
        header_layout.addWidget(self.library_button)


    def show_library_menu(self) -> None:
        """Creates the library menu.
        """

        # Create the menu bar
        context_menu = QMenu(self)

        # Add action to the Library menu
        open_action = QAction("Open", self)
        open_action.setShortcut(QKeySequence("Ctrl+O"))
        open_action.triggered.connect(
            lambda _: self.open_library(context_menu))
        context_menu.addAction(open_action)

        import_action = QAction("Import", self)
        import_action.setShortcut(QKeySequence("Ctrl+I"))
        import_action.triggered.connect(
            lambda _: self.import_library(context_menu))
        context_menu.addAction(import_action)

        export_action = QAction("Export", self)
        export_action.setShortcut(QKeySequence("Ctrl+E"))
        export_action.triggered.connect(
            lambda _: self.export_library(context_menu))
        context_menu.addAction(export_action)

        context_menu.exec(self.library_button.mapToGlobal(
            self.library_button.rect().bottomLeft()))


    def open_library(self, menu: QMenu) -> None:
        """Opens the library popup menu.

        Args:
            menu (QMenu): The menu to close when opening the popup.
        """
        menu.close()

        popup = QWidget()
        popup.setWindowTitle("Library")
        popup.resize(600, 400)

        layout = QVBoxLayout(popup)

        default_label = QLabel("Default Library:")
        default_list = QListWidget()
        self.load_default_meshes(default_list)

        custom_label = QLabel("Custom Library:")
        self.custom_list = QListWidget()

        import_button = QPushButton("Import")
        import_button.clicked.connect(self.import_custom_mesh)

        layout.addWidget(default_label)
        layout.addWidget(default_list)
        layout.addWidget(custom_label)
        layout.addWidget(self.custom_list)
        layout.addWidget(import_button)

        popup.show()
