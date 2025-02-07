"""This module contains the main window of the application."""

import os
from builtins import ValueError
from typing import Optional, List
import numpy as np

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
    QLabel, QSlider, QPushButton, QMessageBox, QLineEdit, QFileDialog
)
from PySide6.QtCore import Qt, QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator

from src.units import Tesla
from src import Config, sofa_instantiator, MeshLoader
from src.mesh_loader import Mode as MeshMode

from gui import MSRHeaderWidget, MSRMaterialGroup

from pathlib import Path
import Sofa.Core


class MainWindow(QMainWindow):
    """Main window of the application."""

    def __init__(self):
        """Initializes the main window.
        """
        super().__init__()

        # Unintialized variables for later code
        self.custom_list = None

        self.setWindowTitle("Soft Robotics Simulation")
        self.resize(1200, 800)

        # Haupt-Widget und Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Header-View
        header_widget = MSRHeaderWidget(self)
        main_layout.addWidget(header_widget)

        # Hauptinhalt - Horizontal Layout
        content_layout = QHBoxLayout()

        # Linke Seitenleiste für Navigation und Parametersteuerung
        sidebar = QGroupBox("Simulation Settings Panel")
        sidebar_layout = QVBoxLayout(sidebar)

        # Materialeigenschaften
        self.material_group = MSRMaterialGroup()
        sidebar_layout.addWidget(self.material_group)

        # Model information
        model_group = QGroupBox("Model Settings")
        model_layout = QVBoxLayout(model_group)

        self.model_name_label = QLabel("Model Name:")
        self.model_nodes_label = QLabel("Model Node Count:")
        self.model_tetrahedra_label = QLabel("Model Tetrahedra Count:")

        model_bounding_box_a_label = QLabel("Constraint Box Lower Corner:")
        self.model_bounding_box_a = QLineEdit()
        self.model_bounding_box_a.setPlaceholderText(
            "Enter as [x, y, z], leave empty for default model")

        model_bounding_box_b_label = QLabel("Constraint Box Upper Corner:")
        self.model_bounding_box_b = QLineEdit()
        self.model_bounding_box_b.setPlaceholderText(
            "Enter as [x, y, z], leave empty for default model")

        model_layout.addWidget(self.model_name_label)
        model_layout.addWidget(self.model_nodes_label)
        model_layout.addWidget(self.model_tetrahedra_label)
        model_layout.addWidget(model_bounding_box_a_label)
        model_layout.addWidget(self.model_bounding_box_a)
        model_layout.addWidget(model_bounding_box_b_label)
        model_layout.addWidget(self.model_bounding_box_b)

        sidebar_layout.addWidget(model_group)

        # Magnetfeldsteuerung
        field_group = QGroupBox("Magnet Field Settings")
        field_layout = QVBoxLayout(field_group)

        self.field_strength_label = QLabel("Magnetic Field Strength (T):")
        self.field_strength_slider = QSlider(Qt.Horizontal)
        self.field_strength_slider.setRange(0, 1000)
        self.field_strength_slider.setValue(500)
        self.field_strength_slider.setTickPosition(QSlider.TicksBelow)
        self.field_strength_slider.setTickInterval(100)
        self.field_strength_slider.valueChanged.connect(
            self.update_field_strength_label)

        field_direction_label = QLabel("Direction (Vector):")
        self.field_direction_input = QLineEdit("[0, -1, 0]")
        self.field_direction_input.setPlaceholderText(
            "Enter direction as [x, y, z]")

        vector_regex = QRegularExpression(
            r"^\s*\[\s*(-?\d+(\.\d+)?\s*,\s*){2}-?\d+(\.\d+)?\s*\]\s*$")
        validator = QRegularExpressionValidator(vector_regex)
        self.field_direction_input.setValidator(validator)
        self.model_bounding_box_a.setValidator(validator)
        self.model_bounding_box_b.setValidator(validator)

        field_layout.addWidget(self.field_strength_label)
        field_layout.addWidget(self.field_strength_slider)
        field_layout.addWidget(field_direction_label)
        field_layout.addWidget(self.field_direction_input)

        sidebar_layout.addWidget(field_group)

        # Schaltfläche zum Anwenden der Parameter
        apply_button = QPushButton("Apply")
        apply_button.clicked.connect(self.apply_parameters)
        sidebar_layout.addWidget(apply_button)

        sidebar.setFixedWidth(400)
        content_layout.addWidget(sidebar)

        # Hauptanzeige für Visualisierung
        visualization_area = QWidget()
        visualization_area.setStyleSheet("background-color: #f0f0f0;")
        content_layout.addWidget(visualization_area)

        main_layout.addLayout(content_layout)

        # Default values
        Config.set_model("beam", 0.02)

    def update_model(self) -> None:
        """Updates the model name in the GUI."""
        # len(self.mech_obj.position.value)  # nodes
        # len(self.topo.tetrahedra.value)  # tetrahedra
        self.model_name_label.setText(f'Model name: {Config.get_name()}')

        root = Sofa.Core.Node("root")
        root.addObject(
            "RequiredPlugin", pluginName='Sofa.Component.IO.Mesh')

        mesh_loader = MeshLoader()
        # elastic_object = ElasticObject(
        #     root, mesh_loader, 0.3, YoungsModulus(1e6), Density(1000))
        mesh_loader.load_file(
            Path(__file__).parents[1] / f'lib/models/{Config.get_name()}.msh', MeshMode.VOLUMETRIC)

        # print(len(root.mech_obj.position.value))
        model_obj = mesh_loader.load_mesh_into(root, MeshMode.VOLUMETRIC)
        self.model_nodes_label.setText(
            f'Model Node Count: {len(model_obj.position.value)}')
        self.model_tetrahedra_label.setText(
            f'Model Tetrahedra Count: {len(model_obj.tetrahedra.value)}')

    def update_field_strength_label(self) -> None:
        """Updates the field strength output based
        on the current position of the slider in tesla values.
        """
        strength_in_tesla = self.field_strength_slider.value() / 10
        formatted_strength = f"{strength_in_tesla:.4f}".rstrip("0").rstrip(".")
        self.field_strength_label.setText(
            f"Magnetic Field Strength: {formatted_strength} T")

    def parse_direction_input(self, text: str) -> Optional[List[float]]:
        """Parses the direction input from the user
        and ensures that it is a valid vector with 3 components.

        Args:
            text (str): Direction input of the user.

        Raises:
            ValueError: Should never be raised as it is catched.

        Returns:
            Optional[List[float]]: The parsed direction vector.
        """

        try:
            clean_values = text.strip("[]() ").replace(
                " ", "").replace(";", ",")
            values = [float(i) for i in clean_values.split(
                ",") if i.strip("- ").replace(".", "").isdigit()]

            if len(values) != 3:
                raise ValueError
            return values
        except ValueError:
            return None

    def apply_parameters(self) -> None:
        """Print the parameters and throws exception if invalid direction input.
        """
        direction = self.parse_direction_input(
            self.field_direction_input.text())
        if direction is None:
            QMessageBox.warning(self, "Error", "Invalid direction.")
            return

        field_strength_val = self.field_strength_slider.value() / 10  # Umrechnung in Tesla
        field_strength = Tesla.from_T(field_strength_val)

        Config.set_show_force(False)
        Config.set_external_forces(True,
                                   np.array([0, -9.81, 0]),
                                   field_strength,
                                   np.array(direction),
                                   np.array([1, 0, 0]))

        params = self.material_group.parameters
        Config.set_material_parameters(params["poissons_ratio"].value(),
                                       params["youngs_modulus"].value(),
                                       params["density"].value(),
                                       params["remanence"].value())

        bounding_box_a = self.parse_direction_input(
            self.model_bounding_box_a.text())
        bounding_box_b = self.parse_direction_input(
            self.model_bounding_box_b.text())

        if bounding_box_a is None or bounding_box_b is None:
            Config.set_default_constraints()
        else:
            Config.set_constraints(
                np.array(bounding_box_a), np.array(bounding_box_b))

        sofa_instantiator.main()

    def import_mesh_file(self) -> None:
        """Imports a custom mesh file.
        """
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Mesh Files (*.obj *.stl)")
        file_dialog.setFileMode(QFileDialog.ExistingFile)

        if file_dialog.exec():
            selected_file = file_dialog.selectedFiles()[0]
            filename = os.path.basename(selected_file)
            self.custom_list.addItem(filename)

            QMessageBox.information(
                self, "Import Success", f"Successfully imported: {filename}")
