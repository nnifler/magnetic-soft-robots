"""
This module bundles functionality around the import popup window.
It provides a GUI to import surface and volumetric mesh models, with options to define names and paths. 
The module also handles file import and format validation.
"""

from typing import Set
from shutil import copy2
from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFileDialog, QGridLayout, QGroupBox,
    QLabel, QPushButton, QLineEdit, QMessageBox, QMainWindow
)
from PySide6.QtCore import Qt
from src.mesh_loader import MeshLoader, Mode
from gui import MSROpenModelsPopup


class MSRModelImportPopup(QWidget):
    """Class defining behaviour of the Import Models popup."""

    def __init__(self, open_models_popup: MSROpenModelsPopup) -> None:
        """Create the Import Models popup menu."""

        super().__init__()

        self.setWindowTitle("Import Models")
        self.resize(600, 200)

        self._mesh_loader = MeshLoader()
        self._selection_widget = open_models_popup

        self.surface_formats = {".stl"}
        # self.surface_formats = MeshLoader.get_supported_meshes(Mode.SURFACE)
        self.volumetric_formats = {".msh"}
        # self.surface_formats = MeshLoader.get_supported_meshes(Mode.VOLUMETRIC)

        self.name_label = QLabel("Model Name:")
        self.name_definition = QLineEdit()

        self.surf_button = QPushButton("Fetch Surface Mesh")
        self.surf_path_label = QLabel("[path not set]")
        self.surf_button.clicked.connect(
            lambda _: self._fetch_path(
                self.surface_formats, self.surf_path_label)
        )
        self.vol_button = QPushButton("Fetch Volumetric Mesh")
        self.vol_path_label = QLabel("[path not set]")
        self.vol_button.clicked.connect(
            lambda _: self._fetch_path(
                self.volumetric_formats, self.vol_path_label)
        )

        def_widget = QGroupBox("Define Model")
        def_layout = QGridLayout(def_widget)
        OFFSET = 1
        def_layout.addWidget(self.name_label, OFFSET-1, 0)
        def_layout.addWidget(self.name_definition, OFFSET-1, 1)
        def_layout.addWidget(self.surf_button, OFFSET, 0)
        def_layout.addWidget(self.surf_path_label, OFFSET, 1)
        def_layout.addWidget(self.vol_button, OFFSET+1, 0)
        def_layout.addWidget(self.vol_path_label, OFFSET+1, 1)

        import_button = QPushButton("Import and Select Model")
        import_button.clicked.connect(
            self._import
        )

        layout = QVBoxLayout(self)
        layout.addWidget(def_widget)
        layout.addWidget(import_button)

    def _fetch_path(self, allowed_suffix: Set[str], label: QLabel) -> None:
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
            str(Path(__file__).parents[1] / "lib/models"),
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

        dst_dir = Path(__file__).parents[1] / "lib/imported_models"
        existing_names = [path.stem for path in dst_dir.iterdir()]
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

            copy2(vol_path_str, dst_dir / f'{name}.msh')
            copy2(surf_path_str, dst_dir / f'{name}.stl')

            if self._selection_widget is None:
                raise ValueError("No MSROpenModelsPopup provided to select.")
            model_list = self._selection_widget.custom_list
            self._selection_widget.load_models(model_list, dst_dir)
            item = model_list.findItems(name, Qt.MatchFlag.MatchExactly)[0]
            index = model_list.indexFromItem(item)
            model_list.activated.emit(index)

            QMessageBox.information(
                self, "Success", "Model imported successfully.")

            # after import success as selection success should come after import success
            self._selection_widget.open_model()
            self.close()

        except (FileNotFoundError, ValueError) as e:
            QMessageBox.warning(self, "Error", f"Failed to import model {e}")
