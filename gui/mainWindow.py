import os
import json
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
    QLabel, QSlider, QDoubleSpinBox, QComboBox, QPushButton, QGridLayout, QMessageBox
)
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
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

        mrs_label = QLabel("MRS")
        mrs_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        header_layout.addWidget(mrs_label, alignment=Qt.AlignLeft)

        self.library_button = QPushButton("Library")
        self.save_button = QPushButton("Speichern")
        header_layout.addStretch()
        header_layout.addWidget(self.library_button)
        header_layout.addWidget(self.save_button)

        main_layout.addWidget(header_widget)

        # Hauptinhalt - Horizontal Layout
        content_layout = QHBoxLayout()

        # Linke Seitenleiste für Navigation und Parametersteuerung
        sidebar = QGroupBox("Navigation und Parametersteuerung")
        sidebar_layout = QVBoxLayout(sidebar)

        # Materialeigenschaften
        material_group = QGroupBox("Materialeigenschaften")
        material_layout = QGridLayout(material_group)

        material_label = QLabel("Material auswählen:")
        self.material_combo_box = QComboBox()
        self.material_combo_box.currentIndexChanged.connect(self.update_material_parameters)

        self.material_data = []  # Platz für JSON-Daten
        self.load_materials_from_json()

        behavior_label = QLabel("Materialverhalten:")
        self.behavior_combo_box = QComboBox()
        self.behavior_combo_box.addItems(["Linear-elastisch", "Plastisch", "Viskoelastisch"])

        young_modulus_label = QLabel("(E) Elastizitätsmodul (Pa):")
        self.young_modulus_spinbox = QDoubleSpinBox()
        self.young_modulus_spinbox.setRange(0, 1e12)
        self.young_modulus_spinbox.setDecimals(2)

        poisson_label = QLabel("(ν) Poisson-Verhältnis:")
        self.poisson_spinbox = QDoubleSpinBox()
        self.poisson_spinbox.setRange(0, 0.5)
        self.poisson_spinbox.setDecimals(2)

        density_label = QLabel("(ρ) Dichte (kg/m³):")
        self.density_spinbox = QDoubleSpinBox()
        self.density_spinbox.setRange(0, 20000)
        self.density_spinbox.setDecimals(0)

        magnetization_label = QLabel("Magnetisierungsstärke (A/m):")
        self.magnetization_spinbox = QDoubleSpinBox()
        self.magnetization_spinbox.setRange(0, 1e7)
        self.magnetization_spinbox.setDecimals(0)

        # Layout für Materialeigenschaften
        material_layout.addWidget(material_label, 0, 0)
        material_layout.addWidget(self.material_combo_box, 0, 1)

        material_layout.addWidget(behavior_label, 1, 0)
        material_layout.addWidget(self.behavior_combo_box, 1, 1)

        material_layout.addWidget(young_modulus_label, 2, 0)
        material_layout.addWidget(self.young_modulus_spinbox, 2, 1)

        material_layout.addWidget(poisson_label, 3, 0)
        material_layout.addWidget(self.poisson_spinbox, 3, 1)

        material_layout.addWidget(density_label, 4, 0)
        material_layout.addWidget(self.density_spinbox, 4, 1)

        material_layout.addWidget(magnetization_label, 5, 0)
        material_layout.addWidget(self.magnetization_spinbox, 5, 1)

        sidebar_layout.addWidget(material_group)

        # Magnetfeldsteuerung
        field_group = QGroupBox("Magnetfeldsteuerung")
        field_layout = QVBoxLayout(field_group)

        field_strength_label = QLabel("Feldstärke (Tesla):")
        self.field_strength_slider = QSlider(Qt.Horizontal)
        self.field_strength_slider.setRange(0, 100)
        self.field_strength_slider.setValue(50)
        self.field_strength_slider.setTickPosition(QSlider.TicksBelow)
        self.field_strength_slider.setTickInterval(10)

        field_direction_label = QLabel("Richtung (Vektor):")
        self.field_direction_input = QLabel("[0, 0, 1]")  # Platzhalter

        field_layout.addWidget(field_strength_label)
        field_layout.addWidget(self.field_strength_slider)
        field_layout.addWidget(field_direction_label)
        field_layout.addWidget(self.field_direction_input)

        sidebar_layout.addWidget(field_group)

        # Schaltfläche zum Anwenden der Parameter
        apply_button = QPushButton("Anwenden")
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
        # Lädt Materialien aus einer JSON-Datei
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
        # Aktualisiert die Parameterfelder basierend auf der Auswahl im ComboBox
        index = self.material_combo_box.currentIndex()
        if 0 <= index < len(self.material_data):
            material = self.material_data[index]
            self.density_spinbox.setValue(material.get("density", 0))
            self.young_modulus_spinbox.setValue(material.get("youngs_modulus", 0))
            self.poisson_spinbox.setValue(material.get("poissons_ratio", 0))
            self.magnetization_spinbox.setValue(material.get("magnetization_strength", 0))

    def apply_parameters(self):
        # Erfassung der Parameterwerte
        material = self.material_combo_box.currentText()
        behavior = self.behavior_combo_box.currentText()
        young_modulus = self.young_modulus_spinbox.value()
        poisson_ratio = self.poisson_spinbox.value()
        density = self.density_spinbox.value()
        magnetization_strength = self.magnetization_spinbox.value()
        field_strength = self.field_strength_slider.value()
        field_direction = self.field_direction_input.text()

        print(f"Material: {material}, Verhalten: {behavior}, Elastizitätsmodul: {young_modulus} Pa, "
              f"Poisson-Verhältnis: {poisson_ratio}, Dichte: {density} kg/m³, Magnetisierungsstärke: {magnetization_strength} A/m, "
              f"Feldstärke: {field_strength} Tesla, Richtung: {field_direction}")

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
