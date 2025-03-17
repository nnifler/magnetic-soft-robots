from __future__ import annotations
"""Main window module for the Magnetic Soft Robotics Simulation.

Provides the graphical user interface (GUI) for configuring and running 
soft robotics simulations. It includes controls for selecting materials, 
adjusting simulation parameters, and visualizing results.

Classes:
    MainWindow: The main application window containing UI elements and 
                parameter management for the simulation.
"""

import multiprocessing as mp
import os
import re
from builtins import ValueError
from typing import Optional, List, Tuple
from pathlib import Path
import numpy as np

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
    QLabel, QSlider, QPushButton, QMessageBox, QLineEdit, QFileDialog, QGridLayout, QTabWidget
)
from PySide6.QtCore import Qt, QRegularExpression, QThread
from PySide6.QtGui import QRegularExpressionValidator
import Sofa.Core
from src.units import Tesla
from src import AnalysisParameters, Config, MeshLoader, sofa_instantiator
from src.mesh_loader import Mode as MeshMode

from gui import MSRHeaderWidget, MSRMaterialGroup, MSRDeformationAnalysisWidget, MSRStressAnalysisWidget


class MainWindow(QMainWindow):
    """Main window of the application.

    This class sets up the graphical user interface (GUI) for the 
    Soft Robotics Simulation, including material selection, 
    simulation controls, and visualization.

    Attributes:
    material_group (MSRMaterialGroup): Widget for material properties.
    deformation_widget (MSRDeformationAnalysisWidget): Widget for deformation analysis.
    field_strength_slider (QSlider): Slider for adjusting the magnetic field strength.
    field_direction_input (QLineEdit): Input field for defining the magnetic field direction.
    """
    class Listener(QThread):
        """Inherits from QThread to monitor calls from the SOFA Simulation.
        """

        def run(self) -> None:
            """Listens for signals from the SOFA process and passes them to the appropriate GUI components.
            """
            call_to_func = {
                # self.stress_analysis.set_min,
                "stress_min": self.parent().stress_analysis.set_min,
                "stress_max": self.parent().stress_analysis.set_max,
                "stress_reset": self.parent().stress_analysis.reset,
                "deform_update": self.parent().deformation_widget.update_results,
                "deform_error": self.parent().deformation_widget.display_input_error,
            }
            while True:
                while not self.parent()._reciever.poll(1):
                    pass
                package = self.parent()._reciever.recv()
                call, args = package
                call_to_func[call](*args)

    def __init__(self):
        """Initialize the main window and set up the UI."""

        super().__init__()

        # Unintialized variables for later code
        self.custom_list = None

        self.setWindowTitle("Soft Robotics Simulation")
        self.resize(500, 800)

        # Main widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Header-View
        header_widget = MSRHeaderWidget(self)
        main_layout.addWidget(header_widget)

        # Main content - Horizontal layout
        content_layout = QHBoxLayout()

        # Left sidebar for navigation and parameter control
        sidebar = QVBoxLayout()
        sidebar_tabs = QTabWidget()
        simulation_settings = QWidget()
        simulation_layout = QVBoxLayout(simulation_settings)
        sidebar_tabs.addTab(simulation_settings, "Simulation Settings")

        # Material properties
        self.material_group = MSRMaterialGroup()
        simulation_layout.addWidget(self.material_group, stretch=3)

        # Model configuration
        model_group = QGroupBox("Model Configuration")
        model_layout = QGridLayout(model_group)

        model_name_label = QLabel("Selected Model:")
        self._model_name = QLabel()
        model_nodes_label = QLabel("Number of Nodes:")
        self._model_nodes = QLabel()
        model_tetrahedra_label = QLabel("Number of Tetrahedra:")
        self._model_tetrahedra = QLabel()

        model_bounding_box_a_label = QLabel("Constraint Box Lower Corner:")
        self._model_bounding_box_a = QLineEdit()
        self._model_bounding_box_a.setPlaceholderText(
            "Enter as [x, y, z], leave empty for default model")

        model_bounding_box_b_label = QLabel("Constraint Box Upper Corner:")
        self._model_bounding_box_b = QLineEdit()
        self._model_bounding_box_b.setPlaceholderText(
            "Enter as [x, y, z], leave empty for default model")

        model_layout.addWidget(model_name_label, 0, 0)
        model_layout.addWidget(self._model_name, 0, 1)
        model_layout.addWidget(model_nodes_label, 1, 0)
        model_layout.addWidget(self._model_nodes, 1, 1)
        model_layout.addWidget(model_tetrahedra_label, 2, 0)
        model_layout.addWidget(self._model_tetrahedra, 2, 1)
        model_layout.addWidget(model_bounding_box_a_label, 3, 0, 1, 2)
        model_layout.addWidget(self._model_bounding_box_a, 4, 0, 1, 2)
        model_layout.addWidget(model_bounding_box_b_label, 5, 0, 1, 2)
        model_layout.addWidget(self._model_bounding_box_b, 6, 0, 1, 2)

        # Magnetic field control
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
        self._model_bounding_box_a.setValidator(validator)
        self._model_bounding_box_b.setValidator(validator)

        field_layout.addWidget(self.field_strength_label)
        field_layout.addWidget(self.field_strength_slider)
        field_layout.addWidget(field_direction_label)
        field_layout.addWidget(self.field_direction_input)

        simulation_layout.addWidget(field_group, stretch=1)
        simulation_layout.addWidget(model_group, stretch=3)

        sidebar.addWidget(sidebar_tabs)

        # Analysis Tab
        analysis_settings = QWidget()
        analysis_layout = QVBoxLayout(analysis_settings)
        sidebar_tabs.addTab(analysis_settings, "Analysis Settings")

        # Space to add to analysis tab
        self.stress_analysis = MSRStressAnalysisWidget(analysis_settings)
        analysis_layout.addWidget(self.stress_analysis)

        self.deformation_widget = MSRDeformationAnalysisWidget()
        analysis_layout.addWidget(self.deformation_widget)

        # Button for applying the parameters
        apply_button = QPushButton("Apply")
        apply_button.clicked.connect(self.apply_parameters)
        sidebar.addWidget(apply_button)

        sidebar_tabs.setFixedWidth(500)
        content_layout.addLayout(sidebar)

        # Main display for visualisation
        visualization_area = QWidget()
        visualization_area.setStyleSheet("background-color: #f0f0f0;")
        content_layout.addWidget(visualization_area)

        main_layout.addLayout(content_layout)

        # Default values
        Config.set_model("butterfly", None, False)

        self._simulation = None
        self._reciever, self._caller = mp.Pipe()
        self._listener = self.Listener(self)
        self.destroyed.connect(self._listener.terminate)
        self._listener.start()

    def update_model(self) -> None:
        """Updates the model value fields in the GUI after setting the model."""
        name = Config.get_name()

        # SOFA to get nodes and tetrahedra
        root = Sofa.Core.Node("root")
        root.addObject(
            "RequiredPlugin", pluginName='Sofa.Component.IO.Mesh')
        mesh_loader = MeshLoader()
        # TODO: still hardcoded mesh file type (GUI - Import Meshes)
        # TODO: hardcodced path --> change for packaging
        mesh_loader.load_file(
            Path(__file__).parents[1] / f'lib/models/{name}.msh', MeshMode.VOLUMETRIC)
        model_obj = mesh_loader.load_mesh_into(root, MeshMode.VOLUMETRIC)

        # updating the values
        node_count = len(model_obj.position.value)
        tetrahedron_count = len(model_obj.tetrahedra.value)
        self._model_name.setText(name)
        self._model_nodes.setText(str(node_count))
        self._model_tetrahedra.setText(str(tetrahedron_count))

    def update_field_strength_label(self) -> None:
        """Update the magnetic field strength label based on the slider value.

        The slider value is divided by 10 to convert it into Tesla
        and displayed with up to four decimal places.
        """
        strength_in_tesla = self.field_strength_slider.value() / 1000
        formatted_strength = f"{strength_in_tesla:.4f}".rstrip("0").rstrip(".")
        self.field_strength_label.setText(
            f"Magnetic Field Strength: {formatted_strength} T")

    def parse_direction_input(self, text: str) -> Optional[List[float]]:
        """Parses the direction input from the user
        and ensures that it is a valid vector with 3 components.

        Args:
            text (str): Direction input of the user.

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
        """Apply the selected parameters and update the simulation configuration.

        This method retrieves material parameters, field strength, and direction 
        from the UI and updates the simulation settings accordingly. 
        If the direction input is invalid, a warning message is displayed.
        """

        direction = self.parse_direction_input(
            self.field_direction_input.text())
        if direction is None:
            QMessageBox.warning(self, "Error", "Invalid direction!")
            return

        field_strength_val = self.field_strength_slider.value() / 1000  # Conversion to Tesla
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
            self._model_bounding_box_a.text())
        bounding_box_b = self.parse_direction_input(
            self._model_bounding_box_b.text())

        if bounding_box_a is None or bounding_box_b is None:
            Config.set_default_constraints()
        else:
            Config.set_constraints(
                np.array(bounding_box_a), np.array(bounding_box_b))

        deformation_widget_enabled, deformation_input_list = self._parse_max_deformation_information()
        if deformation_widget_enabled is None:
            return

        analysis_parameters = AnalysisParameters(self._caller)
        if deformation_widget_enabled:
            analysis_parameters.enable_max_deformation_analysis(
                self.deformation_widget, deformation_input_list)
        else:
            analysis_parameters.disable_max_deformation_analysis()

        show_stress = self.stress_analysis.show_stress
        if show_stress:
            analysis_parameters.enable_stress_analysis(self.stress_analysis)
        else:
            analysis_parameters.disable_stress_analysis()

        Config.set_stress_kwargs(show_stress)
        Config.set_analysis_parameters(analysis_parameters)

        if self._simulation is not None:
            self._simulation.kill()
        self._simulation = mp.Process(target=sofa_instantiator.main)
        self._simulation.start()
        print("simulation process started")

    def _parse_max_deformation_information(self) -> Tuple[bool, List[int | np.ndarray]]:
        """Parses the information from the deformation widget 
        and returns whether it is enabled and the input list.

        Returns:
            Tuple[bool, List[int | np.ndarray]]: A tuple containing
            - A boolean indicating whether the deformation widget is enabled.
            - A list containing the indices or coordinates, depending on the selection mode.
        """
        input_list = []
        deformation_widget_enabled = False
        if self.deformation_widget.is_enabled():
            deformation_widget_enabled = True
            # Check coordinates
            if self.deformation_widget.point_radio_buttons[1].isChecked():
                coords = self.deformation_widget.point_inputs[0].toPlainText()
                # Match with regex
                if not self.deformation_widget.coord_regex.match(coords):
                    QMessageBox.warning(self, "Error", "Invalid coordinates!")
                    return None, None
                # Extract information
                coord_nums = list(
                    map(float, re.findall(r"-?\d+(?:\.\d+)?", coords)))
                # Save coordinates in numpy arrays
                for i in range(0, len(coord_nums), 3):
                    input_list.append(np.array(coord_nums[i:i+3]))

            # Check indices
            if self.deformation_widget.point_radio_buttons[2].isChecked():
                indices = self.deformation_widget.point_inputs[1].toPlainText()
                # Match with regex
                if not self.deformation_widget.indices_regex.match(indices):
                    QMessageBox.warning(self, "Error", "Invalid indices!")
                    return None, None
                # Extract information
                input_list = list(map(int, re.findall(r"\d+", indices)))
        return deformation_widget_enabled, input_list

    def import_mesh_file(self) -> None:
        """Import a custom mesh file and update the model list.

        Opens a file dialog for selecting an OBJ or STL file.
        If a file is successfully imported, it is added to the list
        and a confirmation message is displayed.
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
