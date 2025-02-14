"""This module provides a toolkit for material parameter definition."""

import json
from pathlib import Path
from PySide6.QtWidgets import (
    QGroupBox, QLabel, QDoubleSpinBox, QComboBox, QGridLayout, QMessageBox, QPushButton, QLineEdit
)
from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator
from string import punctuation, whitespace

from src.units import BaseUnit, Density, YoungsModulus, Tesla
from src import JsonMaterialManager


class MSRMaterialParameter():
    """Bundles all information needed for parameter definition. 
    One instance should be created for each parameter.
    Includes widgets and unit management.
    """
    decimal_validator = QRegularExpressionValidator(
        QRegularExpression(r"^-?\d+[.,]?\d*$"))

    def __init__(self, name: str,
                 value_range: tuple[float, float],
                 units: list[str],
                 setter: list,
                 getter: list,
                 step: float = 1.,
                 decimals: int = 4,
                 index: int = 0,

                 ) -> None:
        """Initialize a wrapper for material parameters.

        Args:
            name (str): Descriptive name of the Parameter selection: '(symbol) Parameter Name:'
            value_range (tuple[float, float]): Valid value range (lo, hi)
            units (list[str]): String representations of available units
            setter (list): Unit.from_X methods in the same order as units (if implemented)
            getter (list): Unit.X properties in the same order as units
            step (float, optional): Step size for spinbox. Defaults to 1..
            decimals (int, optional): Decimal places in spinbox. Defaults to 4.
            index (int, optional): Starting index of unit selection. Defaults to 0.
        """
        self.label = QLabel(text=name)
        self.spinbox = QDoubleSpinBox()
        self.unit_selector: QLabel | QComboBox = None

        self._decimals = decimals
        self._units = units
        self._setter = setter
        self._getter = getter

        self.spinbox.setRange(*value_range)
        self.spinbox.setDecimals(decimals)
        self.spinbox.setSingleStep(step)

        self.spinbox.lineEdit().setValidator(MSRMaterialParameter.decimal_validator)
        self.spinbox.lineEdit().editingFinished.connect(
            lambda: self.spinbox.setValue(
                float(self.spinbox.text().replace(",", ".")))
        )

        if len(units) == 0:
            self.unit_selector = QLabel("")
        elif len(units) == 1:
            self.unit_selector = QLabel(f"{units[0]}")
            self._unit_index = 0
        elif len(units) > 1:
            self.unit_selector = QComboBox()
            self.unit_selector.addItems(units)
            self._unit_index = index
            self.unit_selector.setCurrentIndex(self._unit_index)
            self.unit_selector.currentIndexChanged.connect(
                self._change_unit
            )

    def _change_unit(self) -> None:
        """Method called when switching units in the QComboBox.
        """
        if len(self._units) <= 1:
            return

        value = self.spinbox.value()
        unit = self._setter[self._unit_index](value)
        cur_index = self.unit_selector.currentIndex()
        converted_value = self._getter[cur_index].fget(unit)
        self._unit_index = cur_index

        self.spinbox.blockSignals(True)
        self.spinbox.setValue(round(converted_value, self._decimals))
        self.spinbox.blockSignals(False)

    def value(self) -> BaseUnit | float:
        """Returns the value of the corresponding QDoubleSpinBox.

        Returns:
            BaseUnit | float: Subclass of BaseUnit for every implemented unit, float else.
        """
        val = self.spinbox.value()
        if len(self._units) == 0:
            return val

        return self._setter[self._unit_index](val)


class MSRMaterialGroup(QGroupBox):
    """Qt Widget for the material parameter definitions.

    Args:
        QGroupBox: Base class.
    """

    def __init__(self) -> None:
        """Initializes MSRMaterialGroup.
        """
        super().__init__("Material Configuration")
        self._layout = QGridLayout(self)

        material_label = QLabel("Select Material:")
        self._material_combo_box = QComboBox()

        self.material_data: list = []
        # fills self.material_data
        self.load_materials_from_json()

        self._custom_material_data = []
        # fills self._custom_material_data
        self.load_materials_from_json(custom=True)

        # init json material manager
        self._custom_material_manager = JsonMaterialManager()
        self._custom_material_manager.materials = self._custom_material_data.copy()

        behavior_label = QLabel("Material Behavior:")
        self.behavior_combo_box = QComboBox()
        self.behavior_combo_box.addItems(
            ["Linear-Elastic", "Plastic", "Viscoelastic"])

        self.parameters = {
            "youngs_modulus": MSRMaterialParameter(
                name="(E) Young's Modulus:",
                value_range=(0, 1e12),
                units=["Pa", "hPa", "MPa", "GPa"],
                getter=[YoungsModulus.Pa, YoungsModulus.hPa,
                        YoungsModulus.MPa, YoungsModulus.GPa],
                setter=[YoungsModulus.from_Pa, YoungsModulus.from_hPa,
                        YoungsModulus.from_MPa, YoungsModulus.from_GPa],
                index=3,
                step=10,
            ),
            "poissons_ratio": MSRMaterialParameter(
                name="(\u03BD) Poisson's Ratio:",
                value_range=(0, 0.4999),
                units=[],
                setter=[],
                getter=[],
                step=0.1
            ),
            "density": MSRMaterialParameter(
                name="(\u03C1) Density:",
                value_range=(0, 30000),
                units=["kg/m³", "g/cm³", "Mg/m³", "t/m³"],
                getter=[Density.kgpm3, Density.gpcm3,
                        Density.Mgpm3, Density.tpm3],
                setter=[Density.from_kgpm3, Density.from_gpcm3,
                        Density.from_Mgpm3, Density.from_tpm3],
                decimals=2,
            ),
            "remanence": MSRMaterialParameter(
                name="(B<sub>R</sub>) Remanence:",
                value_range=(-2.0, 2.0),
                units=["T"],
                getter=[Tesla.T],
                setter=[Tesla.from_T],
                decimals=3,
            ),
        }

        # export to lib
        self._material_name_input = QLineEdit()
        self._material_name_input.setPlaceholderText("Material Name")
        material_save_button = QPushButton("Save")
        material_save_button.clicked.connect(self._save_current_material)

        self._material_combo_box.currentIndexChanged.connect(
            self.update_material_parameters)

        self._layout.addWidget(material_label, 0, 0)
        self._layout.addWidget(self._material_combo_box, 0, 1)

        self._layout.addWidget(behavior_label, 1, 0)
        self._layout.addWidget(self.behavior_combo_box, 1, 1)

        for row, param in enumerate(self.parameters.values(), start=2):
            self._layout.addWidget(param.label, row, 0)
            self._layout.addWidget(param.spinbox, row, 1)
            self._layout.addWidget(param.unit_selector, row, 2)

        row = len(self.parameters) + 2
        self._layout.addWidget(self._material_name_input, row+1, 0, 1, 2)
        self._layout.addWidget(material_save_button, row+1, 2)

    def _save_current_material(self) -> None:
        """Saves the current material to the custom JSON file."""
        mat_name = self._material_name_input.text()

        if mat_name.strip(punctuation+whitespace) == "":
            QMessageBox.warning(self, "Error", "Please enter a material name.")
            return
        if mat_name in [m.get("name", "") for m in self.material_data]:
            QMessageBox.warning(
                self, "Error", "Material name already exists in default materials.")
            return
        if mat_name in [m.get("name", "") for m in self._custom_material_data]:
            QMessageBox.warning(
                self, "Error", "Material name already exists in custom materials.")
            return

        self._custom_material_manager.append_material(
            mat_name,
            self.parameters["density"].value(),
            self.parameters["youngs_modulus"].value(),
            self.parameters["poissons_ratio"].value(),
            self.parameters["remanence"].value()
        )

        self._custom_material_manager.save_to_json(
            Path(__file__).parents[1] / 'lib/materials/custom.json')
        self._material_combo_box.clear()
        # load self.material_data
        self.load_materials_from_json(custom=False)
        # load self._custom_material_data
        self.load_materials_from_json(custom=True)
        self._material_combo_box.setCurrentIndex(
            self._material_combo_box.count() - 1)
        QMessageBox.information(self, "Material saved",
                                "Material saved successfully.")

    def load_materials_from_json(self, custom=False) -> None:
        """Loads the materials from the JSON file.

        Args:
            custom (bool, optional): If True, loads the custom JSON file. Defaults to False.
        """
        # root directory of the project
        current_dir = Path(__file__).parents[1]
        # Path to the JSON file
        # by moving one directory up from the current directory to the selected folder
        data_path = current_dir / "lib/materials" / \
            ('custom.json' if custom else 'default.json')
        if custom and not data_path.exists():
            return
        json_file_path = data_path
        print(f"Looking for JSON file at: {json_file_path}")

        try:
            with open(json_file_path, "r", encoding="utf-8") as file:
                material_data = json.load(file)

            for material in material_data:
                self._material_combo_box.addItem(
                    material.get("name", "Unknown Material"))

            # resave the data to self
            if custom:
                self._custom_material_data = material_data
            else:
                self.material_data = material_data

        except FileNotFoundError:
            QMessageBox.warning(
                self, "Error", "Materials JSON file not found.")
        except json.JSONDecodeError as e:
            QMessageBox.warning(
                self, "Error", f"Error decoding JSON file:\n{e}")

    def update_material_parameters(self) -> None:
        """Updates the material parameters with the data from the opened JSON file.
        """
        current_material_index = self._material_combo_box.currentIndex()
        material = None
        if 0 <= current_material_index < len(self.material_data):
            material = self.material_data[current_material_index]
        elif 0 <= current_material_index < len(self._custom_material_data) + len(self.material_data):
            material = self._custom_material_data[
                current_material_index - len(self.material_data)]
        else:
            return

        # Dichte mit Umrechnung aktualisieren
        density_param = self.parameters["density"]
        density = Density.from_kgpm3(material.get("density", 0))
        current_density_index = density_param.unit_selector.currentIndex()
        vals = [density.kgpm3, density.gpcm3, density.Mgpm3, density.tpm3]
        converted_density = vals[current_density_index]
        density_param.spinbox.blockSignals(True)
        density_param.spinbox.setValue(round(converted_density, 2))
        density_param.spinbox.blockSignals(False)

        # Young's Modulus mit Umrechnung aktualisieren

        youngs_modulus_param = self.parameters["youngs_modulus"]
        youngs_modulus = YoungsModulus.from_Pa(
            material.get("youngs_modulus", 0))
        current_modulus_index = youngs_modulus_param.unit_selector.currentIndex()
        vals = [youngs_modulus.Pa, youngs_modulus.hPa,
                youngs_modulus.MPa, youngs_modulus.GPa]
        converted_modulus = vals[current_modulus_index]
        youngs_modulus_param.spinbox.blockSignals(True)
        youngs_modulus_param.spinbox.setValue(round(converted_modulus, 4))
        youngs_modulus_param.spinbox.blockSignals(False)

        # poisson's ratio and remanence set manually
        self.parameters["poissons_ratio"].spinbox.setValue(
            material.get("poissons_ratio", 0))
        self.parameters["remanence"].spinbox.setValue(
            material.get("remanence", 0))
