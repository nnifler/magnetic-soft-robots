import json
from bs4 import BeautifulSoup
import re

# Magnetische Feldkonstante (μ0) in T·m/A
MU_0 = 4 * 3.141592653589793 * 1e-7

materials = [
    {
        "name": "Silicone Rubber",
        "density": 1100,  # in kg/m³
        "youngs_modulus": 1e6,  # in Pa
        "poissons_ratio": 0.49,  # dimensionslos
        "remanence": 0 * MU_0,  # in T

    },
    {
        "name": "Neodymium Powder",
        "density": 7500,  # in kg/m³
        "youngs_modulus": 1.6e10,  # in Pa
        "poissons_ratio": 0.3,  # dimensionslos
        "remanence": 1.2e6 * MU_0,  # in T

    },
    {
        "name": "Magnetic Silicone Composite",
        "density": 1800,  # in kg/m³
        "youngs_modulus": 5e6,  # in Pa
        "poissons_ratio": 0.45,  # dimensionslos
        "remanence": 2.5e4 * MU_0,  # in T

    }
]

with open('lib/materials/matweb_export.html') as ht:
    soup = BeautifulSoup(ht, 'html.parser')

# Find all rows
rows = soup.find_all('tr', class_=['altrow', ''])


def calculate_average(range_str):
    numbers = [float(num.replace(',', '.'))
               for num in re.findall(r'\d+\.?\d*', range_str)]
    if len(numbers) == 2:
        return sum(numbers) / 2
    elif len(numbers) == 1:
        return numbers[0]
    else:
        return None


for row in rows:
    columns = row.find_all('td')
    if not columns:
        continue
    # material_name = columns[2].get_text(strip=True).split('\n')[0].strip()
    material_name = columns[2].get_text(strip=True)
    material_link = 'https://www.matweb.com'+columns[2].find('a')['href']
    range_property_1 = calculate_average(columns[3].get_text(strip=True))*1e9
    range_property_2 = calculate_average(columns[5].get_text(strip=True))*1e3
    range_property_3 = calculate_average(columns[7].get_text(strip=True))

    materials.append({
        'name': material_name,
        'url': material_link,
        'youngs_modulus': range_property_1,
        'density': range_property_2,
        'poissions_ratio': range_property_3,
        'remanence': 0.  # nicht wirklich angebbar?
    })

# JSON-Datei speichern
file_name = "lib/materials/magnetic_soft_robot_materials.json"
with open(file_name, "w") as file:
    json.dump(materials, file, indent=4)

print(f"JSON file '{file_name}' created successfully!")
