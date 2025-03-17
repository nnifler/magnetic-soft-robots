"""Main window module for the Magnetic Soft Robotics Simulation.

Provides the graphical user interface (GUI) for configuring and running
soft robotics simulations. It includes controls for selecting materials,
adjusting simulation parameters, and visualizing results.

Classes:
    MainWindow: The main application window containing UI elements and
                parameter management for the simulation.
"""


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
from PySide6.QtCore import Qt
import Sofa.Core

from src.units import Tesla
from src import AnalysisParameters, Config, MeshLoader, sofa_instantiator
from src.mesh_loader import Mode as MeshMode

from gui import MSRHeaderWidget, MSRMaterialGroup, MSRDeformationAnalysisWidget, MSRMaterialParameter, MSRStressAnalysisWidget


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

    def __init__(self):
        """Initialize the main window and set up the UI."""

        super().__init__()

        # Unintialized variables for later code
        self.custom_list = None
        self._custom_model = False

        self.setWindowTitle("Magnetic Soft Robotics Simulation")
        self.resize(400, 600)

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
        self._model_custom_label = QLabel("Default")
        self._model_custom_label.setDisabled(True)
        model_nodes_label = QLabel("Number of Nodes:")
        self._model_nodes = QLabel()
        model_tetrahedra_label = QLabel("Number of Tetrahedra:")
        self._model_tetrahedra = QLabel()

        self._model_bounding_box_a_label = QLabel(
            "Constraint Box Lower Corner:")
        self._model_bounding_box_a = QLineEdit()
        self._model_bounding_box_a.setPlaceholderText(
            "Enter as [x, y, z]")

        self._model_bounding_box_b_label = QLabel(
            "Constraint Box Upper Corner:")
        self._model_bounding_box_b = QLineEdit()
        self._model_bounding_box_b.setPlaceholderText(
            "Enter as [x, y, z]")

        self._update_bounding_box_enabled()

        model_layout.addWidget(model_name_label, 0, 0)
        model_layout.addWidget(self._model_name, 0, 1)
        model_layout.addWidget(self._model_custom_label, 0, 2)
        model_layout.addWidget(model_nodes_label, 1, 0)
        model_layout.addWidget(self._model_nodes, 1, 1)
        model_layout.addWidget(model_tetrahedra_label, 2, 0)
        model_layout.addWidget(self._model_tetrahedra, 2, 1)
        model_layout.addWidget(self._model_bounding_box_a_label, 3, 0)
        model_layout.addWidget(self._model_bounding_box_a, 3, 1, 1, 2)
        model_layout.addWidget(self._model_bounding_box_b_label, 4, 0)
        model_layout.addWidget(self._model_bounding_box_b, 4, 1, 1, 2)

        # Magnetic field control
        field_group = QGroupBox("Magnet Field Settings")
        field_layout = QGridLayout(field_group)

        self._slider_multiplier = 1000  # base unit (mT)

        # Input field for magnetic flux density
        self._field_strength = MSRMaterialParameter("(B) Magnetic Flux Density:", (0, 5), [
            'T'], [Tesla.from_T], [Tesla.T], .01, 4, 0)
        self._field_strength.spinbox.setValue(1.)
        self._field_strength.spinbox.valueChanged.connect(
            lambda value: self._field_strength_update(  # Update slider
                value,
                spinbox=False,
                slider=True))

        self.field_strength_slider = QSlider(Qt.Horizontal)
        self.field_strength_slider.setRange(0, 5*self._slider_multiplier)
        self.field_strength_slider.setValue(1*self._slider_multiplier)
        self.field_strength_slider.setTickPosition(QSlider.TicksBelow)
        self.field_strength_slider.setTickInterval(self._slider_multiplier)
        field_strength_max = QLabel("5 T")
        field_strength_max.setAlignment(Qt.AlignRight)
        field_strength_min = QLabel("0 T")
        field_strength_min.setAlignment(Qt.AlignLeft)
        self.field_strength_slider.valueChanged.connect(
            lambda value: self._field_strength_update(  # update fine slider and spinbox
                value/self._slider_multiplier,
                spinbox=True,
                slider=False))

        field_direction_label = QLabel("Direction (Vector):")
        self.field_direction_input = QLineEdit("[0, -1, 0]")
        self.field_direction_input.setPlaceholderText(
            "Enter as [x, y, z]")

        # label spinbox
        field_layout.addWidget(self._field_strength.label, 0, 0)
        # spinbox
        field_layout.addWidget(self._field_strength.spinbox, 0, 1)
        # unit selector
        field_layout.addWidget(self._field_strength.unit_selector, 0, 2)
        # coarse slider
        field_layout.addWidget(self.field_strength_slider, 1, 0, 1, 3)
        # slider min (0)
        field_layout.addWidget(field_strength_min, 2, 0)
        # slider max (5)
        field_layout.addWidget(field_strength_max, 2, 2)
        # label direction
        field_layout.addWidget(field_direction_label, 5, 0)
        # direction input ([x, y, z])
        field_layout.addWidget(self.field_direction_input, 5, 1)

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

        sidebar_tabs.setFixedWidth(400)
        content_layout.addLayout(sidebar)

        # Main display for visualisation
        visualization_area = QWidget()
        content_layout.addWidget(visualization_area)

        main_layout.addLayout(content_layout)

        # Default values
        Config.set_model("butterfly", None, False)

    def _update_bounding_box_enabled(self) -> None:
        """Enables or disables the bounding box inputs based on the model type."""
        self._model_bounding_box_a_label.setDisabled(not self._custom_model)
        self._model_bounding_box_b_label.setDisabled(not self._custom_model)
        self._model_bounding_box_a.setDisabled(not self._custom_model)
        self._model_bounding_box_b.setDisabled(not self._custom_model)

    def update_model(self, custom_model: bool) -> None:
        """Updates the model value fields in the GUI after setting the model.

        Args:
            custom_model (bool): Whether the model is a custom model.
        """
        name = Config.get_name()
        self._custom_model = custom_model

        # Disable bounding box inputs for default models

        if self._custom_model:
            self._model_custom_label.setText("Custom")
        else:
            self._model_custom_label.setText("Default")

        self._update_bounding_box_enabled()

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
        self._model_name.setText(name.rsplit('/', maxsplit=1)[-1])
        self._model_nodes.setText(str(node_count))
        self._model_tetrahedra.setText(str(tetrahedron_count))

    def _field_strength_update(self, strength: float, spinbox: bool,
                               slider: bool) -> None:
        """Updates the different field strength input fields in the GUI.

        Args:
            strength (float): The new field strength value in Tesla.
            spinbox (bool): Whether to update the spinbox.
            slider (bool): Whether to update the coarse slider.
        """
        try:  # block signals to prevent infinite loops
            self._field_strength.spinbox.blockSignals(True)
            self.field_strength_slider.blockSignals(True)
            if spinbox:
                self._field_strength.spinbox.setValue(strength)
            if slider:
                self.field_strength_slider.setValue(
                    strength * self._slider_multiplier)
        finally:
            self._field_strength.spinbox.blockSignals(False)
            self.field_strength_slider.blockSignals(False)

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

        Config.set_show_force(True)
        Config.set_external_forces(True,
                                   np.array([0, -9.81, 0]),
                                   self._field_strength.value(),
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

        if not self._custom_model:  # Default model
            Config.set_default_constraints()
        elif bounding_box_a is None or bounding_box_b is None:
            QMessageBox.warning(self, "Error", "Invalid bounding box!")
            return
        else:
            Config.set_constraints(
                np.array(bounding_box_a), np.array(bounding_box_b))

        deformation_widget_enabled, deformation_input_list = \
            self._parse_max_deformation_information()

        analysis_parameters = AnalysisParameters()
        if deformation_widget_enabled:
            analysis_parameters.enable_max_deformation_analysis(
                self.deformation_widget, deformation_input_list)

        show_stress = self.stress_analysis.show_stress
        if show_stress:
            analysis_parameters.enable_stress_analysis(self.stress_analysis)
        else:
            analysis_parameters.disable_stress_analysis()
        Config.set_stress_kwargs(show_stress)

        sofa_instantiator.main(analysis_parameters)

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
