"""
This module bundles functionality around the import popup window.
It provides a GUI to iport surface and volumetric mesh models, witj options to define names and paths. The module also includes methodes to handle file import and format validation.
"""

from typing import Set
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

        self._mesh_loader = MeshLoader()

        self.surface_formats = {".stl"}
        # self.mesh_loader.get_supported_meshes(Mode.SURFACE)
        self.volumetric_formats = {".msh"}
        # self.mesh_loader.get_supported_meshes(Mode.VOLUMETRIC)

        self.name_label = QLabel("Model Name:")
        self.name_definition = QLineEdit()

        self.surf_button = QPushButton("Fetch Surface Mesh")
        self.surf_path_label = QLabel("[path not set]")
        self.surf_button.clicked.connect(
            lambda _: self.fetch_path(
                self.surface_formats, self.surf_path_label)
        )
        self.vol_button = QPushButton(f"Fetch Volumetric Mesh")
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

    def fetch_path(self, allowed_suffix: Set[str], label: QLabel) -> None:
        """Opens a QFileDialog to find files to import. Writes resulting path in label

        For input errors, it opens: 
            QMessageBox: If no file is selected.

        Args:
            allowed_suffix (set): Defines which files are accepted.
            label (QLabel): The label to write file path in.
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

        For input errors, it opens: 
            QMessageBox: If no name is provided.
            QMessageBox: If no mesh is selected.
            QMessageBox: If import fails.
        """
        name = self.name_definition.text()

        if not name:
            QMessageBox.warning(
                self, "Warning", "Please provide a name for the model.")
            return

        name = '_'.join(name.strip().split(sep=" "))

        existing_files = os.listdir(os.path.dirname(
            __file__)+"/../lib/imported_models")
        existing_names = [os.path.splitext(file)[0] for file in existing_files]
        if name in existing_names:
            QMessageBox.warning(
                self, "Warning", "Model with this name already exists.")
            return

        vol_path_str = self.vol_path_label.text()
        surf_path_str = self.surf_path_label.text()

        # vol_path = Path(vol_path_str)
        # surf_path = Path(surf_path_str)

        if vol_path_str in {"", "[path not set]"} or surf_path_str in {"", "[path not set]"}:
            QMessageBox.warning(
                self, "Warning", "At least one mesh path not set.")
            return

        try:
            # use mesh loader for file integrity checks
            self._mesh_loader.load_file(Path(surf_path_str), Mode.SURFACE)
            self._mesh_loader.load_file(Path(vol_path_str), Mode.VOLUMETRIC)

            dst_dir = os.path.dirname(__file__)+"/../lib/imported_models/"
            os.makedirs(dst_dir, exist_ok=True)

            copy2(vol_path_str, str(dst_dir)+f'{name}.msh')
            copy2(surf_path_str, str(dst_dir)+f'{name}.stl')

            QMessageBox.information(
                self, "Success", "Model imported successfully.")
            self.close()

        except (FileNotFoundError, ValueError) as e:
            QMessageBox.warning(self, "Error", f"Failed to import model {e}")
