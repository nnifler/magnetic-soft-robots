"""
This module provides functionality for the Import Models popup window.

It allows users to import surface and volumetric mesh models, with options to define
names and file paths. The module includes methods to handle file selection, import,
and format validation.

Classes:
    MSRModelImportPopup: Defines the behavior and interface for the Import Models popup.
"""
import os
from pathlib import Path
from shutil import copy2
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFileDialog, QPushButton,
    QMessageBox, QGridLayout, QGroupBox, QLineEdit
)
from src.mesh_loader import Mode, MeshLoader


class MSRModelImportPopup(QWidget):
    """Defines the behavior and interface for the Import Models popup.."""

    def __init__(self) -> None:
        """Initializes the Import Models popup"""

        super().__init__()

        self.setWindowTitle("Import Models")
        self.resize(600, 300)

        self.mesh_loader = MeshLoader()
        self.setup_import_ui()

    def setup_import_ui(self) -> None:
        """Sets up the user interface for the Import Models popup."""
        layout = QVBoxLayout(self)

        self.name_label = QLabel("Model Name:")
        self.name_definition = QLineEdit()

        self.surface_path_label = QLabel("No file selected")
        self.surface_button = QPushButton(
            f"Fetch {'Surface'} Mesh"
        )
        self.surface_button.clicked.connect(
            lambda _: self.fetch_path(Mode.SURFACE, self.surface_path_label)
        )

        self.volumetric_path_label = QLabel("No file selected")
        self.volumetric_button = QPushButton(f"Fetch {'Volumetric'} Mesh")
        self.volumetric_button.clicked.connect(
            lambda: self.fetch_path(
                Mode.VOLUMETRIC, self.volumetric_path_label)
        )

        group_box = QGroupBox("Model Selection")
        group_layout = QGridLayout(group_box)

        group_layout.addWidget(self.name_label, 0, 0)
        group_layout.addWidget(self.name_definition, 0, 1)

        group_layout.addWidget(self.surface_path_label, 1, 1)
        group_layout.addWidget(self.surface_button, 1, 0)

        group_layout.addWidget(self.volumetric_path_label, 2, 1)
        group_layout.addWidget(self.volumetric_button, 2, 0)

        import_button = QPushButton("Import Model")
        import_button.clicked.connect(
            self.import_models
        )

        layout.addWidget(group_box)
        layout.addWidget(import_button)

    def fetch_path(self, mode: Mode, label: QLabel) -> None:
        """Selects and validates a file path for the given mesh mode.

        Args:
            mode (Mode): The mode of the mesh.
            label (QLabel): The label to display the path.
        """
        extensions = " ".join(
            [f"*{extension}" for extension in self.get_supported_meshes(mode)])
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Path...",
            "lib/models",
            f"Model Files ({extensions})"
        )

        if not file_path:
            QMessageBox.warning(self, "No file selected",
                                "Please select a file.")
            return

        try:
            self.mesh_loader.validate_mesh_file(Path(file_path), mode)
            label.setText(file_path)
        except (FileNotFoundError, ValueError) as e:
            QMessageBox.warning(self, "Invalid File", str(e))

    def import_models(self) -> None:
        """Handles the process of importing models.

        Validates the input data, checks for existing models, copies the files to the
        library, and informs the user about the success or failure of the import process.
        """
        name = self.name_definition.text()

        if not name:
            QMessageBox.warning(
                self, "Warning", "Please provide a name for the model.")
            return

        name = '_'.join(name.strip().split(sep=" "))

        lib_path = Path(__file__).parent.parent / "lib" / "imported_models"
        if lib_path.exists():
            existing_files = os.listdir(lib_path)
            existing_names = {os.path.splitext(
                file)[0] for file in existing_files}
            if f"{name}_surface" in existing_names or f"{name}_volumetric" in existing_names:
                QMessageBox.warning(
                    self, "Warning", "Model with this name already exists.")
                return

        surface_path = self.surface_path_label.text()
        volumetric_path = self.volumetric_path_label.text()

        if surface_path in {"", "No file selected"} or volumetric_path in {"", "No file selected"}:
            QMessageBox.warning(self, "Error", "Please select both files.")
            return

        try:
            self.mesh_loader.load_file(Path(surface_path), Mode.SURFACE)
            self.mesh_loader.load_file(Path(volumetric_path), Mode.VOLUMETRIC)

            lib_path.mkdir(parents=True, exist_ok=True)
            surface_destination = lib_path / \
                f"{name}_surface{Path(surface_path).suffix}"
            volumetric_destination = lib_path / \
                f"{name}_volumetric{Path(volumetric_path).suffix}"

            copy2(surface_path, surface_destination)
            copy2(volumetric_path, volumetric_destination)

            QMessageBox.information(
                self, "Success", "Models imported successfully.")
            self.close()

        except (FileNotFoundError, ValueError) as e:
            QMessageBox.warning(self, "Error",
                                f"Import failed: {e}")

    def get_supported_meshes(self, mode: Mode) -> set:
        """Returns the supported mesh formats for the specified mode.

        Args:
            mode (Mode): The mode of the mesh (surface or volumetric).

        Returns:
            set: A set of supported file extensions.
        """
        if mode is Mode.SURFACE:
            return {".obj", ".stl", ".vtk", ".off", ".msh"}
        elif mode is Mode.VOLUMETRIC:
            return {".msh", ".off", ".vtk"}
        return set()
