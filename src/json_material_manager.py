"""Module for managing materials in JSON format."""

import json
from pathlib import Path
import re
from bs4 import BeautifulSoup
from scipy.constants import mu_0  # in T·m/A
from src.units import Density, YoungsModulus, Tesla


class JsonMaterialManager:
    """Class for managing json materials."""

    # define class constants
    # list of default testing materials
    DEFAULT_MATERIALS = [
        {
            'name': 'Silicone Rubber',
            'density': 1100,  # in kg/m³
            'youngs_modulus': 1e6,  # in Pa
            'poissons_ratio': 0.49,  # dimensionless
            'remanence': 0 * mu_0,  # in T
        },
        {
            'name': 'Neodymium Powder',
            'density': 7500,  # in kg/m³
            'youngs_modulus': 1.6e10,  # in Pa
            'poissons_ratio': 0.3,  # dimensionless
            'remanence': 1.2e6 * mu_0,  # in T
        },
        {
            'name': 'Magnetic Silicone Composite',
            'density': 1800,  # in kg/m³
            'youngs_modulus': 5e6,  # in Pa
            'poissons_ratio': 0.45,  # dimensionless
            'remanence': 2.5e4 * mu_0,  # in T
        },
    ]

    def __init__(self) -> None:
        """Initializes the JsonMaterialManager."""
        self.materials = []

    def append_material(self, name: str,
                        density: Density,
                        youngs_modulus: YoungsModulus,
                        poissons_ratio: float,
                        remanence: Tesla) -> None:
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
    def save_default_materials() -> None:
        """Rebuilds the default json material file."""
        material_manager = JsonMaterialManager()
        material_manager.load_default_materials()
        material_manager.save_to_json(
            Path(__file__).parents[1] / 'lib/materials/default.json')

    def save_to_json(self, file_path: Path) -> None:
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

    def load_matweb_table(self, file_path: Path
                          = Path(__file__).parents[1] / 'lib/materials/matweb_export.html') -> None:
        """Loads material data from a HTML file. Supported are tables from matweb.com.

        Args:
            file_path (Path, optional): Path to the HTML file.
                Defaults to Path(__file__).parents[1]/'lib/matweb_export.html'.
        """
        with open(file_path, encoding='utf-8') as html_source:
            html_dom = BeautifulSoup(html_source, 'html.parser')

            # Find all rows
            rows = html_dom.find_all('tr')
            for row in rows:
                columns = row.find_all('td')
                if not columns:
                    continue

                name = columns[2].get_text(strip=True)
                # get the local href to the material and complete it to global url
                url = 'https://www.matweb.com' + \
                    columns[2].find('a')['href']
                youngs_modulus = YoungsModulus.from_GPa(self._calculate_mean(
                    columns[3].get_text(strip=True)))
                density = Density.from_gpcm3(self._calculate_mean(
                    columns[5].get_text(strip=True)))
                poissons_ratio = self._calculate_mean(
                    columns[7].get_text(strip=True))

                self.materials.append({
                    'name': name,
                    'url': url,  # not supported in self.append_material
                    'youngs_modulus': youngs_modulus.Pa,
                    'density': density.kgpm3,
                    'poissons_ratio': poissons_ratio,
                    'remanence': 0.  # not available
                })

    def load_default_materials(self) -> None:
        """Loads default materials."""
        self.materials = self.DEFAULT_MATERIALS
        self.load_matweb_table()


# Run the script to save the default materials
if __name__ == '__main__':
    JsonMaterialManager.save_default_materials()
