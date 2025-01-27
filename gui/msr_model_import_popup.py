"""
This module bundles functionality around the import popup window.
It provides a GUI to iport surface and volumetric mesh models, witj options to define names and paths. The module also includes methodes to handle file import and format validation.
"""

from shutil import copy2
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFileDialog, QGridLayout, QGroupBox,
    QLabel, QPushButton, QLineEdit, QMessageBox
)
import os
from src import Config
from pathlib import Path
from src.mesh_loader import MeshLoader, Mode


class MSRModelImportPopup(QWidget):
    """Class defining behaviour of the Import Models popup."""

    def __init__(self) -> None:
        """Create the Import Models popup menu."""

        super().__init__()

        self.setWindowTitle("Import Models")
        self.resize(600, 200)

        self.mesh_loader = MeshLoader()

        self.surface_formats = self.get_supported_meshes(Mode.SURFACE)
        self.volumetric_formats = self.get_supported_meshes(Mode.VOLUMETRIC)

        self.name_label = QLabel("Model Name:")
        self.name_definition = QLineEdit()

        self.surf_button = QPushButton(f"Fetch {'Surface'} Mesh")
        self.surf_path_label = QLabel("[path not set]")
        self.surf_button.clicked.connect(
            lambda _: self.fetch_path(
                self.surface_formats, self.surf_path_label)
        )
        self.vol_button = QPushButton(f"Fetch {'Volumetric'} Mesh")
        self.vol_path_label = QLabel("[path not set]")
        self.vol_button.clicked.connect(
            lambda _: self.fetch_path(
                self.volumetric_formats, self.vol_path_label)
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

    def fetch_path(self, allowed_suffix: set, label: QLabel) -> None:
        """Opens a QFileDialog to find files to import. Writes resulting path in label

        Args:
            allowed_suffix (set): Defines which files are accepted.
            label (QLabel): The label to write file path in.

        Raises: 
            QMessageBox: If no file is selected.
        """
        extensions = " ".join(
            [f"*{extension}" for extension in allowed_suffix])
        filename = QFileDialog.getOpenFileName(
            self,
            "Select Path...",
            "lib/models",
            f"Mesh Files ({extensions})",
        )
        if filename:
            label.setText(filename[0])
        else:
            QMessageBox.warning(self, "No file selected",
                                "Please select a file to import.")

    def _import(self) -> None:
        """Copies entries into import mesh folder.

        Raises:
            QMessageBox: If no name is provided.
            QMessageBox: If no mesh is selected.
            QMessageBox: If import fails.
        """
        name = '_'.join(self.name_definition.text().strip().split(sep=" "))
        if not name:
            QMessageBox.warning(
                self, "Warning", "Please provide a name for the model.")
            return

        vol_path = self.vol_path_label.text()
        surf_path = self.surf_path_label.text()

        if vol_path in {"", "[path not set]"} and surf_path in {"", "[path not set]"}:
            QMessageBox.warning(
                self, "Warning", "Please select at least one mesh type.")
            return

        try:
            if surf_path not in {"", "[path not set]"}:
                self.mesh_loader.load_file(Path(surf_path), Mode.SURFACE)
            if vol_path not in {"", "[path not set]"}:
                self.mesh_loader.load_file(Path(vol_path), Mode.VOLUMETRIC)

            dst = f"lib/imported_models/{name}"
            os.makedirs("lib/imported_models", exist_ok=True)
            if vol_path not in {"", "[path not set]"}:
                copy2(vol_path, dst+'.msh')
            if surf_path not in {"", "[path not set]"}:
                copy2(surf_path, dst+'.stl')

            QMessageBox.information(
                self, "Success", "Model imported successfully.")
            self.close()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to import model {e}")

    def get_supported_meshes(self, mode: Mode) -> set:
        """Returns supported mesh formats for the given mesh type."""
        if mode == Mode.SURFACE:
            return {".obj", ".stl", ".vtk", ".off", ".msh"}
        elif mode == Mode.VOLUMETRIC:
            return {".msh", ".off", ".vtk"}
        return set()
