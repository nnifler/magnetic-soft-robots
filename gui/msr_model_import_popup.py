"""This module bundles functionality around the import popup window"""

from shutil import copy2
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFileDialog, QGridLayout, QGroupBox, QLabel, QPushButton, QLineEdit
)
from src import Config


class MSRModelImportPopup(QWidget):
    """Class defining behaviour of the Import Models popup."""

    def __init__(self) -> None:
        """Create the Import Models popup menu."""

        super().__init__()

        self.setWindowTitle("Import Models")
        self.resize(600, 200)

        self.name_label = QLabel("Model Name:")
        self.name_definition = QLineEdit()

        self.surf_button = QPushButton(f"Fetch {'Surface'} Mesh")
        self.surf_path_label = QLabel("[path not set]")
        self.surf_button.clicked.connect(
            lambda _: self.fetch_path("Mesh (*.stl)", self.surf_path_label)
        )
        self.vol_button = QPushButton(f"Fetch {'Volumetric'} Mesh")
        self.vol_path_label = QLabel("[path not set]")
        self.vol_button.clicked.connect(
            lambda _: self.fetch_path("Mesh (*.msh)", self.vol_path_label)
        )

        def_widget = QGroupBox("Define Model")
        def_layout = QGridLayout(def_widget)
        i = 1
        def_layout.addWidget(self.name_label, i-1, 0)
        def_layout.addWidget(self.name_definition, i-1, 1)
        def_layout.addWidget(self.surf_button, i, 0)
        def_layout.addWidget(self.surf_path_label, i, 1)
        def_layout.addWidget(self.vol_button, i+1, 0)
        def_layout.addWidget(self.vol_path_label, i+1, 1)

        import_button = QPushButton("Import Model")
        import_button.clicked.connect(
            self._import
        )

        layout = QVBoxLayout(self)
        layout.addWidget(def_widget)
        layout.addWidget(import_button)

    def fetch_path(self, allowed_suffix: str, label: QLabel) -> None:
        """Opens a QFileDialog to find files to import. Writes resulting path in label

        Args:
            allowed_suffix (str): Defines which files are accepted.
            label (QLabel): The label to write file path in.
        """
        filename = QFileDialog.getOpenFileName(
            self,
            "Select Path...",
            "lib/models",
            allowed_suffix,
        )
        label.setText(filename[0])

    def _import(self) -> None:
        """Copies entries into import mesh folder."""
        name = '_'.join(self.name_definition.text().strip().split(sep=" "))
        dst = f"lib/imported_models/{name}"
        vol_path = self.vol_path_label.text()
        surf_path = self.surf_path_label.text()

        if vol_path == "" or vol_path == "[path not set]":
            return
        if surf_path == "" or surf_path == "[path not set]":
            return

        copy2(vol_path, dst+'.msh')
        copy2(surf_path, dst+'.stl')
