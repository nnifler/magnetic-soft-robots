from src.elastic_body import ElasticObject
from src.units.Density import Density
from src.units.YoungsModulus import YoungsModulus

class MaterialLoader:
    def __init__(self, eo: ElasticObject):
        self._eo = eo
        self._material_values = {
            # "name": "Magnetic Silicone Composite",
            "density": 0.,
            "youngs_modulus": 0,
            "poissons_ratio": 0.,
            "remanence": 0,
        }   #TODO: remanence not in material data

        self._dirty: bool = False

    def set_density(self, value: Density):
        """set material density"""
        self._material_values['density'] = value.kgpm3
        self._dirty = True

    def set_youngs_modulus(self, value: YoungsModulus):
        """set material's young's modulus"""
        self._material_values['youngs_modulus'] = value.Pa
        self._dirty = True

    #TODO: add unit
    def set_poissons_ratio(self, value: float):
        """set poissons ratio"""
        self._material_values['poissons_ratio'] = value
        self._dirty = True

    #TODO: add remanence unit (Tesla)
    def set_remanence(self, value: float):
        """set remanence"""
        self._material_values['remanence'] = value
        self._dirty = True


    def update_elastic_object(self):
        if not self._dirty:
            return

        self._eo.diagonal_mass.setDataValues(massDensity=self._material_values['density'])
        self._eo.FEM_force_field.setDataValues(
            youngModulus=self._material_values['youngs_modulus'],
            poissonRatio=self._material_values['poissons_ratio'],
        )
        self._eo.remanence = self._material_values['remanence']

        self._dirty = False


    ### deprecated

    def set_one(self, parameter: str, val):
        """unsupported"""
        if not parameter in self._material_values.keys():
            raise ValueError("unknown material parameter")
        self._material_values[parameter] = val


    def set_all(self, material_info: dict):
        """unsupported"""
        if not material_info.keys() == self._material_values.keys():
            raise ValueError(f"parameter mismatch. expected {self._material_values.keys()}, but found {material_info.keys()}")

        self._material_values = material_info
