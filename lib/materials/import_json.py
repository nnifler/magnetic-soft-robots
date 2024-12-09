import json

materials = [
    {
        "name": "Silicone Rubber",
        "density": 1100,  # in kg/m³
        "youngs_modulus": 1e6,  # in Pa
        "poissons_ratio": 0.49,  # dimensionslos
        "magnetization_strength": 0,  # in A/m

    },
    {
        "name": "Neodymium Powder",
        "density": 7500,  # in kg/m³
        "youngs_modulus": 1.6e10,  # in Pa
        "poissons_ratio": 0.3,  # dimensionslos
        "magnetization_strength": 1.2e6,  # in A/m
        
    },
    {
        "name": "Magnetic Silicone Composite",
        "density": 1800,  # in kg/m³
        "youngs_modulus": 5e6,  # in Pa
        "poissons_ratio": 0.45,  # dimensionslos
        "magnetization_strength": 2.5e4,  # in A/m
        
    }
]

# JSON-Datei speichern
file_name = "magnetic_soft_robot_materials.json"
with open(file_name, "w") as file:
    json.dump(materials, file, indent=4)

print(f"JSON file '{file_name}' created successfully!")
