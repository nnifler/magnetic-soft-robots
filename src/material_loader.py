from src.elastic_body import ElasticObject
from src.units.Density import Density
from src.units.YoungsModulus import YoungsModulus
# used for commented code:
# from numbers import Number
# from typing import Dict


class MaterialLoader:
    def __init__(self, eo: ElasticObject):
        self._eo = eo
        self._material_values = {
            # "name": "Magnetic Silicone Composite",
            "density": 0.,
            "youngs_modulus": 0,
            "poissons_ratio": 0.,
            "remanence": 0,
        }  # TODO: remanence not in material data

        self._dirty: bool = False

    def set_elastic_object(self, eo: ElasticObject) -> None:
        """Sets the connected ElasticObject anew.
        Helpful for initialization.

        Args:
            eo (ElasticObject): elastic object to load materials into
        """
        self._eo = eo

    # TODO needed?
    # def get_elastic_object(self) -> ElasticObject:
    #     """Returns current elastic object.

    #     Returns:
    #         ElasticObject: current elastic object
    #     """
    #     return self._eo

    def set_density(self, value: Density) -> None:
        """Sets density.

        Args:
            value (Density): density to be set
        """
        self._material_values['density'] = value.kgpm3
        self._dirty = True

    def get_density(self) -> Density:
        """Returns current density.

        Raises:
            ValueError: if read is dirty

        Returns:
            Density: current density
        """
        if self._dirty:
            raise ValueError('Dirty read.')
        return Density(self._material_values['density'])

    def set_youngs_modulus(self, value: YoungsModulus) -> None:
        """Sets Young's modulus.

        Args:
            value (YoungsModulus): Young's modulus to be set
        """
        self._material_values['youngs_modulus'] = value.Pa
        self._dirty = True

    def get_youngs_modulus(self) -> YoungsModulus:
        """Returns current density.

        Raises:
            ValueError: if read is dirty

        Returns:
            YoungsModulus: current Young's modulus
        """
        if self._dirty:
            raise ValueError('Dirty read.')
        return YoungsModulus(self._material_values['youngs_modulus'])

    # TODO: add unit
    def set_poissons_ratio(self, value: float) -> None:
        """Sets poissons ratio.

        Args:
            value (float): Poisson's ratio to be set
        """
        self._material_values['poissons_ratio'] = value
        self._dirty = True

    def get_poissons_ratio(self) -> float:
        """Returns current Poisson's ratio.

        Raises:
            ValueError: if read is dirty

        Returns:
            float: current Poisson's ratio
        """
        if self._dirty:
            raise ValueError('Dirty read.')
        return self._material_values['poissons_ratio']

    # TODO: add remanence unit (Tesla)
    def set_remanence(self, value: float) -> None:
        """Sets remanence.

        Args:
            value (float): remanence to be set
        """
        self._material_values['remanence'] = value
        self._dirty = True

    # TODO: add unit
    def get_remanence(self) -> float:
        """Returns current remanence ratio.

        Raises:
            ValueError: if read is dirty

        Returns:
            float: current remanence ratio
        """
        if self._dirty:
            raise ValueError('Dirty read.')
        return self._material_values['remanence']

    def update_elastic_object(self) -> None:
        """Updates the elastic object if changes occurred.
        """
        if not self._dirty:
            return

        self._eo.diagonal_mass.setDataValues(
            massDensity=self._material_values['density'])
        self._eo.FEM_force_field.setDataValues(
            youngModulus=self._material_values['youngs_modulus'],
            poissonRatio=self._material_values['poissons_ratio'],
        )
        self._eo.remanence = self._material_values['remanence']

        self._dirty = False

    # TODO: maybe useful for lib to directly set json format?
    # unused
    # def set_one(self, material_property: str, value: Number):
    #     """Sets one material `property` directly to a `value`.

    #     Args:
    #         material_property (str): material property to be changed
    #         value (Number): new value

    #     Raises:
    #         ValueError: if material property is unknown
    #     """
    #     if not material_property in self._material_values.keys():
    #         raise ValueError("unknown material property")
    #     self._material_values[material_property] = value

    # unused
    # def set_all(self, material_info: Dict[str, Number]) -> None:
    #     """Sets all material values.

    #     Args:
    #         material_info (Dict[str, Number]): dict with all material properties to be set

    #     Raises:
    #         ValueError: if not all materials properties are given
    #     """
    #     if not material_info.keys() == self._material_values.keys():
    #         raise ValueError(
    #             f"parameter mismatch. expected {self._material_values.keys()}, but found {material_info.keys()}")

    #     self._material_values = material_info
