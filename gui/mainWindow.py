import os
import sys
import json
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QListWidget,
    QPushButton,
    QMessageBox,
    QLabel,
    QSplitter,
    QFrame,
)
from PySide6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Fenster-Einstellungen
        self.setWindowTitle("SOFA GUI")
        self.setGeometry(100, 100, 1200, 800)

        # Zentrale Widget-Struktur
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Splitter für flexibles Layout
        splitter = QSplitter(Qt.Horizontal, self)
        main_layout.addWidget(splitter)

        # Linker Bereich (Library)
        self.library_box = QGroupBox("Library", self)
        library_layout = QVBoxLayout()
        self.library_box.setLayout(library_layout)

        self.sofa_label = QLabel("Sample text: Ready to launch SOFA", self)
        self.sofa_button = QPushButton("Launch SOFA", self)
        self.sofa_button.clicked.connect(self.launch_sofa)
        library_layout.addWidget(self.sofa_label)
        library_layout.addWidget(self.sofa_button)

        splitter.addWidget(self.library_box)

        # Zentraler Bereich (SOFA-Anzeige)
        sofa_frame = QFrame(self)
        sofa_frame.setFrameShape(QFrame.StyledPanel)
        sofa_frame.setStyleSheet("background-color: lightgray;")  # Platzhalter für SOFA-Fenster
        splitter.addWidget(sofa_frame)

        # Rechter Bereich (ausklappbare Widgets)
        right_widget = QSplitter(Qt.Vertical, self)

        # Models Widget
        self.models_list = QListWidget(self)
        self.models_list.setObjectName("Models")
        models_group = QGroupBox("Models")
        models_layout = QVBoxLayout()
        models_layout.addWidget(self.models_list)
        models_group.setLayout(models_layout)
        right_widget.addWidget(models_group)

        # Materials Widget
        self.materials_list = QListWidget(self)
        self.materials_list.setObjectName("Materials")
        materials_group = QGroupBox("Materials")
        materials_layout = QVBoxLayout()
        materials_layout.addWidget(self.materials_list)
        materials_group.setLayout(materials_layout)
        right_widget.addWidget(materials_group)


        splitter.addWidget(right_widget)
        splitter.setStretchFactor(1, 3)

        # Inhalte laden
        self.load_materials_from_json()

    def load_materials_from_json(self):
        # Lädt Materialien aus einer JSON-Datei und zeigt sie in der Materials-Liste an.
        data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../lib/materials/magnetic_soft_robot_materials.json")
        json_file_path = data_path
        print(f"Looking for JSON file at: {json_file_path}")


        try:
            # JSON-Datei laden
            with open(json_file_path, "r") as file:
                materials = json.load(file)

            # Liste aktualisieren
            self.materials_list.clear()
            for material in materials:
                name = material.get("name", "Unknown Material")
                density = material.get("density", "N/A")
                youngs_modulus = material.get("youngs_modulus", "N/A")
                poissons_ratio = material.get("poissons_ratio", "N/A")
                self.materials_list.addItem(f"{name} - Density: {density} kg/m³, Young's Modulus: {youngs_modulus} Pa, Poisson's Ratio: {poissons_ratio}")

        except FileNotFoundError:
            QMessageBox.warning(self, "Error", "Materials JSON file not found.")
        except json.JSONDecodeError as e:
            QMessageBox.warning(self, "Error", f"Error decoding JSON file:\n{e}")

   

    def launch_sofa(self):
        # Platzhalter für SOFA-Start.
        QMessageBox.information(self, "Launch SOFA", "SOFA simulation would start here!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())



       
    