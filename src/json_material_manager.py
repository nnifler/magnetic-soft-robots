"""This module imports material data from a HTML file and saves it as a JSON file."""

import json
import re
from bs4 import BeautifulSoup
import numpy as np
from pathlib import Path
from src.units import Density, YoungsModulus, Tesla


class JsonMaterialManager:
    """Class for managing json materials."""

    # define class constants
    # physical constant: vacuum permeability (μ₀) in T·m/A
    # TODO?: replace with scipy.constants.value('vacuum mag. permeability')
    MU_0 = 4 * np.pi * 1e-7
    # list of default testing materials
    DEFAULT_MATERIALS = [
        {
            'name': 'Silicone Rubber',
            'density': 1100,  # in kg/m³
            'youngs_modulus': 1e6,  # in Pa
            'poissons_ratio': 0.49,  # dimensionless
            'remanence': 0 * MU_0,  # in T
        },
        {
            'name': 'Neodymium Powder',
            'density': 7500,  # in kg/m³
            'youngs_modulus': 1.6e10,  # in Pa
            'poissons_ratio': 0.3,  # dimensionless
            'remanence': 1.2e6 * MU_0,  # in T
        },
        {
            'name': 'Magnetic Silicone Composite',
            'density': 1800,  # in kg/m³
            'youngs_modulus': 5e6,  # in Pa
            'poissons_ratio': 0.45,  # dimensionless
            'remanence': 2.5e4 * MU_0,  # in T
        },
    ]

    def __init__(self):
        self.materials = []

    def append_material(self, name: str, density: Density, youngs_modulus: YoungsModulus, poissons_ratio: float, remanence: Tesla) -> None:
        """Appends a material to the list of materials.

        Args:
            name (str): The name of the material.
            density (Density): The density of the material.
            youngs_modulus (YoungsModulus): The Young's modulus of the material.
            poissons_ratio (float): The Poisson's ratio of the material.
            remanence (Tesla): The remanence of the material.
        """
        self.materials.append({
            'name': name,
            'density': density.kgpm3,
            'youngs_modulus': youngs_modulus.Pa,
            'poissons_ratio': poissons_ratio,
            'remanence': remanence.T
        })

    @staticmethod
    def save_default_materials():
        """Saves the default materials as a JSON file."""
        material_manager = JsonMaterialManager()
        material_manager.load_default_materials()
        material_manager.save_to_json(
            Path(__file__).parents[1] / 'lib/materials/default.json')

    def save_to_json(self, file_path: Path):
        """Saves the loaded material data as a JSON file.

        Args:
            file_path (Path): Path to the JSON file.
        """
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(self.materials, json_file, indent=4)
            json_file.write('\n')  # trailing newline

    def _calculate_mean(self, range_str: str) -> float:
        """Calculates mean from string with a range of numbers.

        Args:
            range_str (str): String with a range of numbers. (e.g. '1.2-1.4')

        Raises:
            ValueError: If the range string is invalid.

        Returns:
            float: Mean of the numbers in the range.
        """
        numbers = [float(num.replace(',', '.'))
                   for num in re.findall(r'\d+\.?\d*', range_str)]
        if len(numbers) == 2:
            return sum(numbers) / 2
        if len(numbers) == 1:
            return numbers[0]
        raise ValueError(f'Invalid range string: {range_str}')

    def load_matweb_table(self, file_path: Path = Path(__file__).parents[1] / 'lib/materials/matweb_export.html'):
        """Loads material data from a HTML file. Supported are tables from matweb.com.

        Args:
            file_path (Path, optional): Path to the HTML file. Defaults to Path(__file__).parents[1]/'lib/matweb_export.html'.
        """
        with open(file_path, encoding='utf-8') as html_source:
            html_dom = BeautifulSoup(html_source, 'html.parser')

            # Find all rows
            rows = html_dom.find_all('tr', class_=['altrow', ''])
            for row in rows:
                columns = row.find_all('td')
                if not columns:
                    continue

                name = columns[2].get_text(strip=True)
                # get the local href to the material and complete it to global url
                url = 'https://www.matweb.com' + \
                    columns[2].find('a')['href']
                youngs_modulus = self._calculate_mean(
                    columns[3].get_text(strip=True))*1e9  # GPa -> Pa
                density = self._calculate_mean(
                    columns[5].get_text(strip=True))*1e3  # g/cm³ -> kg/m³
                poissions_ratio = self._calculate_mean(
                    columns[7].get_text(strip=True))

                self.materials.append({
                    'name': name,
                    'url': url,
                    'youngs_modulus': youngs_modulus,
                    'density': density,
                    'poissons_ratio': poissions_ratio,
                    'remanence': 0.  # not available
                })

    def load_default_materials(self):
        """Loads default materials."""
        self.materials = self.DEFAULT_MATERIALS
        self.load_matweb_table()


if __name__ == '__main__':
    JsonMaterialManager.save_default_materials()
