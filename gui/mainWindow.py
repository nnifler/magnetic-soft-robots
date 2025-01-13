import os
import json
from builtins import ValueError
import numpy as np

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
    QLabel, QSlider, QDoubleSpinBox, QComboBox, QPushButton, QGridLayout, QMessageBox, QLineEdit
)
from PySide6.QtCore import Qt
from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator

from src.units.YoungsModulus import YoungsModulus
from src.units.Density import Density
from src.config import Config
from src import sofa_instantiator

class MainWindow(QMainWindow):
    def __init__(self):
        """Initializes the main window."""
        super().__init__()

        self.setWindowTitle("Soft Robotics Simulation")
        self.resize(1200, 800)

        # Haupt-Widget und Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Header-View
        header_widget = QWidget()
        header_widget.setFixedHeight(30)  # Maximal 1 cm Höhe
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(5, 0, 5, 0)
        header_layout.setSpacing(5)  # Minimaler Abstand zwischen Buttons

        msr_label = QLabel("MSR")
        msr_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        header_layout.addWidget(msr_label, alignment=Qt.AlignLeft)

        self.library_button = QPushButton("Library")
        self.save_button = QPushButton("Save")
        header_layout.addStretch()
        header_layout.addWidget(self.library_button)
        header_layout.addWidget(self.save_button)

        main_layout.addWidget(header_widget)

        # Hauptinhalt - Horizontal Layout
        content_layout = QHBoxLayout()

        # Linke Seitenleiste für Navigation und Parametersteuerung
        sidebar = QGroupBox("Navigation and Settings Panel")
        sidebar_layout = QVBoxLayout(sidebar)

        # Materialeigenschaften
        material_group = QGroupBox("Material Configuration")
        material_layout = QGridLayout(material_group)

        material_label = QLabel("Select Material:")
        self.material_combo_box = QComboBox()

        self.material_data = []  # Platz für JSON-Daten
        self.load_materials_from_json()

        behavior_label = QLabel("Material Behavior:")
        self.behavior_combo_box = QComboBox()
        self.behavior_combo_box.addItems(["Linear-Elastic", "Plastic", "Viscoelastic"])

        young_modulus_label = QLabel("(E) Young's Modulus:")
        self.young_modulus_spinbox = QDoubleSpinBox()
        self.young_modulus_spinbox.setRange(0, 1e12)
        self.young_modulus_spinbox.setDecimals(4)
        self.unit_selector_modulus = QComboBox()
        self.unit_selector_modulus.addItems(["Pa", "hPa", "MPa", "GPa"])
        self.unit_selector_modulus.setCurrentIndex(3)
        self.prev_modulus_index = 3
        self.unit_selector_modulus.currentIndexChanged.connect(self.update_modulus_unit)

        poisson_label = QLabel("(ν) Poisson Ratio:")
        self.poisson_spinbox = QDoubleSpinBox()
        self.poisson_spinbox.setRange(0, 0.4999)
        self.poisson_spinbox.setDecimals(4)

        density_label = QLabel("(ρ) Density:")
        self.density_spinbox = QDoubleSpinBox()
        self.density_spinbox.setRange(0, 30000)
        self.density_spinbox.setDecimals(2)
        self.unit_selector_density = QComboBox()
        self.unit_selector_density.addItems(["kg/m³", "g/cm³", "Mg/m³", "T/m³"])
        self.unit_selector_density.setCurrentIndex(0)
        self.prev_density_index = 0
        self.unit_selector_density.currentIndexChanged.connect(self.update_density_unit)

        self.material_combo_box.currentIndexChanged.connect(self.update_material_parameters)

        remanence_label = QLabel("Remanence (T):")
        self.remanence_spinbox = QDoubleSpinBox()
        self.remanence_spinbox.setRange(-2.0, 2.0)
        self.remanence_spinbox.setDecimals(3)

        # Layout für Materialeigenschaften
        material_layout.addWidget(material_label, 0, 0)
        material_layout.addWidget(self.material_combo_box, 0, 1)

        material_layout.addWidget(behavior_label, 1, 0)
        material_layout.addWidget(self.behavior_combo_box, 1, 1)

        material_layout.addWidget(young_modulus_label, 2, 0)
        material_layout.addWidget(self.young_modulus_spinbox, 2, 1)
        material_layout.addWidget(self.unit_selector_modulus, 2, 2)

        material_layout.addWidget(poisson_label, 3, 0)
        material_layout.addWidget(self.poisson_spinbox, 3, 1)

        material_layout.addWidget(density_label, 4, 0)
        material_layout.addWidget(self.density_spinbox, 4, 1)
        material_layout.addWidget(self.unit_selector_density, 4, 2)

        material_layout.addWidget(remanence_label, 5, 0)
        material_layout.addWidget(self.remanence_spinbox, 5, 1)

        sidebar_layout.addWidget(material_group)

        # Magnetfeldsteuerung
        field_group = QGroupBox("Magnet Field Settings")
        field_layout = QVBoxLayout(field_group)

        self.field_strength_label = QLabel("Magnetic Field Strength (Tesla):")
        self.field_strength_slider = QSlider(Qt.Horizontal)
        self.field_strength_slider.setRange(0, 1000)
        self.field_strength_slider.setValue(500)
        self.field_strength_slider.setTickPosition(QSlider.TicksBelow)
        self.field_strength_slider.setTickInterval(100)
        self.field_strength_slider.valueChanged.connect(self.update_field_strength_label)

        field_direction_label = QLabel("Direction (Vector):")
        self.field_direction_input = QLineEdit("[0, 0, 1]")
        self.field_direction_input.setPlaceholderText("Enter direction as [x, y, z]")

        vector_regex = QRegularExpression(r"^\s*\[\s*(-?\d+(\.\d+)?\s*,\s*){2}-?\d+(\.\d+)?\s*\]\s*$")
        validator = QRegularExpressionValidator(vector_regex)
        self.field_direction_input.setValidator(validator)

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

    def load_materials_from_json(self):
        """Loads materials from a JSON file"""
        data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../lib/materials/magnetic_soft_robot_materials.json")
        json_file_path = data_path
        print(f"Looking for JSON file at: {json_file_path}")

        try:
            with open(json_file_path, "r") as file:
                self.material_data = json.load(file)

            self.material_combo_box.clear()
            for material in self.material_data:
                self.material_combo_box.addItem(material.get("name", "Unknown Material"))

        except FileNotFoundError:
            QMessageBox.warning(self, "Error", "Materials JSON file not found.")
        except json.JSONDecodeError as e:
            QMessageBox.warning(self, "Error", f"Error decoding JSON file:\n{e}")

    def update_material_parameters(self):
        """Updates the material parameters with the data from the opened JSON file"""
        index = self.material_combo_box.currentIndex()
        if 0 <= index < len(self.material_data):
            material = self.material_data[index]

            # Dichte mit Umrechnung aktualisieren
            density = Density.fromkgpm3(material.get("density", 0))
            current_density_index = self.unit_selector_density.currentIndex()
            vals = [density.kgpm3, density.gpcm3, density.Mgpm3, density.tpm3]
            converted_density = vals[current_density_index]
            self.density_spinbox.blockSignals(True)
            self.density_spinbox.setValue(round(converted_density, 2))
            self.density_spinbox.blockSignals(False)

            # Young's Modulus mit Umrechnung aktualisieren
            youngs_modulus = YoungsModulus.fromPa(material.get("youngs_modulus", 0))
            current_modulus_index = self.unit_selector_modulus.currentIndex()
            vals = [youngs_modulus.Pa, youngs_modulus.hPa, youngs_modulus.MPa, youngs_modulus.GPa]
            converted_modulus = vals[current_modulus_index]
            self.young_modulus_spinbox.blockSignals(True)
            self.young_modulus_spinbox.setValue(round(converted_modulus, 4))
            self.young_modulus_spinbox.blockSignals(False)

            # Poisson's Ratio und Remanenz direkt setzen
            self.poisson_spinbox.setValue(material.get("poissons_ratio", 0))
            self.remanence_spinbox.setValue(material.get("remanence", 0))

    def update_modulus_unit(self):
        """Updates the modulus unit if the unit size is changed"""
        value = self.young_modulus_spinbox.value()
        youngs_modulus = [
            YoungsModulus.fromPa(int(value)),
            YoungsModulus.fromhPa(value),
            YoungsModulus.fromMPa(value),
            YoungsModulus.fromGPa(value)
        ][self.prev_modulus_index]
        vals = [
            youngs_modulus.Pa,
            youngs_modulus.hPa,
            youngs_modulus.MPa,
            youngs_modulus.GPa
        ]
        cur_index = self.unit_selector_modulus.currentIndex()
        converted_value = vals[cur_index]
        self.prev_modulus_index = cur_index

        self.young_modulus_spinbox.blockSignals(True)
        self.young_modulus_spinbox.setValue(round(converted_value, 4))
        self.young_modulus_spinbox.blockSignals(False)

    def update_density_unit(self):
        """Updates the density unit if the unit size is changed"""
        value = self.density_spinbox.value()
        density = [
            Density.fromkgpm3(value),
            Density.fromgpcm3(value),
            Density.fromMgpm3(value),
            Density.fromtpm3(value)
        ][self.prev_density_index]
        vals = [
            density.kgpm3,
            density.gpcm3,
            density.Mgpm3,
            density.tpm3
        ]
        cur_index = self.unit_selector_density.currentIndex()
        converted_value = vals[cur_index]
        self.prev_density_index = cur_index
        
        self.density_spinbox.blockSignals(True)
        self.density_spinbox.setValue(round(converted_value, 2))
        self.density_spinbox.blockSignals(False)

    def update_field_strength_label(self):
        """Updates the field strength output based on the current position of the slider in tesla values"""
        strength_in_tesla = self.field_strength_slider.value() / 10
        self.field_strength_label.setText(f"Magnetic Field Strength: {strength_in_tesla:.4f} T")

    def parse_direction_input(self, text: str):
        """
        Parses the direction input from the user

        Arguments:
        - text: direction input of the user
        """
        try:
            values = [float(i) for i in map(lambda x: x.strip(), text[1:-1].split(","))]
            if len(values) != 3:
                raise ValueError
            return values
        except ValueError:
            return None

    def apply_parameters(self):
        """Print the parameters and throws exception if invalid direction input"""
        direction = self.parse_direction_input(self.field_direction_input.text())
        if direction is None:
            QMessageBox.warning(self, "Error", "Invalid direction.")
            return

        # Erfassung der Parameterwerte
        #material = self.material_combo_box.currentText()
        #behavior = self.behavior_combo_box.currentText()
        youngs_modulus_val = self.young_modulus_spinbox.value()
        youngs_modulus = [
            YoungsModulus.fromPa(int(youngs_modulus_val)),
            YoungsModulus.fromhPa(youngs_modulus_val),
            YoungsModulus.fromMPa(youngs_modulus_val),
            YoungsModulus.fromGPa(youngs_modulus_val)
        ][self.unit_selector_modulus.currentIndex()]
        poisson_ratio = self.poisson_spinbox.value()
        density_val = self.density_spinbox.value()
        density = [
            Density.fromkgpm3(density_val),
            Density.fromgpcm3(density_val),
            Density.fromMgpm3(density_val),
            Density.fromtpm3(density_val)
        ][self.unit_selector_density.currentIndex()]
        remanence = self.remanence_spinbox.value()
        field_strength = self.field_strength_slider.value() / 10  # Umrechnung in Tesla

        normalized_dir = np.array(direction) / np.linalg.norm(np.array(direction))

        Config.set_show_force(True)
        Config.set_model("butterfly_disected",
                         0.02)
        Config.set_external_forces(True,
                                   np.array([0, -9.81, 0]),
                                   field_strength,
                                   normalized_dir,
                                   np.array([1, 0, 0]))
        Config.set_material_parameters(poisson_ratio,
                                       youngs_modulus,
                                       density,
                                       remanence)
        Config.set_plugin_list(['Sofa.Component.Collision.Detection.Algorithm',
            'Sofa.Component.Collision.Detection.Intersection',
            'Sofa.Component.Collision.Geometry',
            'Sofa.Component.Collision.Response.Contact',
            'Sofa.Component.Constraint.Projective',
            'Sofa.Component.IO.Mesh',
            'Sofa.Component.LinearSolver.Iterative',
            'Sofa.Component.Mapping.Linear',
            'Sofa.Component.Mass',
            'Sofa.Component.ODESolver.Backward',
            'Sofa.Component.SolidMechanics.FEM.Elastic',
            'Sofa.Component.StateContainer',
            'Sofa.Component.Topology.Container.Dynamic',
            'Sofa.Component.Visual',
            'Sofa.GL.Component.Rendering3D',
            'Sofa.Component.AnimationLoop',
            'Sofa.Component.LinearSolver.Direct',
            'Sofa.Component.Constraint.Lagrangian.Correction',
            'Sofa.Component.Topology.Mapping',
            'Sofa.Component.MechanicalLoad'
        ])

        sofa_instantiator.main()
        #print(f"Material: {material}, Verhalten: {behavior}, Elastizitätsmodul: {young_modulus} GPa, "
        #      f"Poisson-Verhältnis: {poisson_ratio}, Dichte: {density} kg/m³, Remanenz: {remanence} T, "
        #      f"Feldstärke: {field_strength} Tesla, Richtung: {direction}")
