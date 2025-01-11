import json

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

# JSON-Datei speichern
file_name = "magnetic_soft_robot_materials.json"
with open(file_name, "w") as file:
    json.dump(materials, file, indent=4)

print(f"JSON file '{file_name}' created successfully!")
