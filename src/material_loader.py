# ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾ #
#                        MSR, Magnetic Soft Robotics Simulation                        #
#   Copyright (C) 2025 Julius Hahnewald, Heiko Hellkamp, Finn Schubert, Carla Wehner   #
#                                                                                      #
# This program is free software; you can redistribute it and/or                        #
# modify it under the terms of the GNU Lesser General Public                           #
# License as published by the Free Software Foundation; either                         #
# version 2.1 of the License, or (at your option) any later version.                   #
#                                                                                      #
# This program is distributed in the hope that it will be useful,                      #
# but WITHOUT ANY WARRANTY; without even the implied warranty of                       #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU                    #
# Lesser General Public License for more details.                                      #
#                                                                                      #
# You should have received a copy of the GNU Lesser General Public                     #
# License along with this program; if not, write to the Free Software                  #
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301            #
# USA                                                                                  #
# ------------------------------------------------------------------------------------ #
# Contact information: finn.s.schubert@gmail.com                                       #
# ____________________________________________________________________________________ #

"""This module provides a class to load material properties into an ElasticObject."""

# used for commented code:
# from numbers import Number
# from typing import Dict
from . import ElasticObject
from .units import Density, YoungsModulus, Tesla


class MaterialLoader:
    """Class to load material properties into an ElasticObject."""

    def __init__(self, elastic_object: ElasticObject) -> None:
        """Initializes the MaterialLoader.

        Args:
            elastic_object (ElasticObject): The ElasticObject to load materials into.
        """
        self._eo = elastic_object
        self._material_values = {
            # "name": "Magnetic Silicone Composite",
            "density": 0.,
            "youngs_modulus": 0,
            "poissons_ratio": 0.,
            "remanence": 0,
        }

        self._dirty: bool = False

    def set_elastic_object(self, elastic_object: ElasticObject) -> None:
        """Sets the connected ElasticObject anew. Helpful for initialization.

        Args:
            elastic_object (ElasticObject): The ElasticObject to load materials into.
        """
        self._eo = elastic_object

    # TODO needed?
    # def get_elastic_object(self) -> ElasticObject:
    #     """Returns current elastic object.

    #     Returns:
    #         ElasticObject: current elastic object
    #     """
    #     return self._eo

    def set_density(self, value: Density) -> None:
        """Sets density in the connected ElasticObject.

        Args:
            value (Density): Density to be set
        """
        self._material_values['density'] = value.kgpm3
        self._dirty = True

    def get_density(self) -> Density:
        """Returns current density from the connected ElasticObject.
        If the read is dirty, updates the connected ElasticObject.

        Returns:
            Density: current density.
        """
        if self._dirty:
            self.update_elastic_object()
        return Density(self._material_values['density'])

    def set_youngs_modulus(self, value: YoungsModulus) -> None:
        """Sets Young's modulus in the connected ElasticObject.

        Args:
            value (YoungsModulus): Young's modulus to be set in the connected ElasticObject.
        """
        self._material_values['youngs_modulus'] = value.Pa
        self._dirty = True

    def get_youngs_modulus(self) -> YoungsModulus:
        """Returns current density from the connected ElasticObject.
        If the read is dirty, updates the connected ElasticObject.

        Returns:
            YoungsModulus: current Young's modulus.
        """
        if self._dirty:
            self.update_elastic_object()
        return YoungsModulus(self._material_values['youngs_modulus'])

    # TODO: add unit
    def set_poissons_ratio(self, value: float) -> None:
        """Sets poissons ratio in the connected ElasticObject.

        Args:
            value (float): Poisson's ratio to be set in the connected ElasticObject.
        """
        self._material_values['poissons_ratio'] = value
        self._dirty = True

    def get_poissons_ratio(self) -> float:
        """Returns current Poisson's ratio from the connected ElasticObject.
        If the read is dirty, updates the connected ElasticObject.

        Returns:
            float: current Poisson's ratio
        """
        if self._dirty:
            self.update_elastic_object()
        return self._material_values['poissons_ratio']

    def set_remanence(self, value: Tesla) -> None:
        """Sets remanence in the connected ElasticObject.

        Args:
            value (Tesla): Remanence to be set in the connected ElasticObject.
        """
        self._material_values['remanence'] = value.T
        self._dirty = True

    def get_remanence(self) -> Tesla:
        """Returns current remanence from the connected ElasticObject.
        If the read is dirty, updates the connected ElasticObject.

        Returns:
            Tesla: current remanence
        """
        if self._dirty:
            self.update_elastic_object()
        return Tesla(self._material_values['remanence'])

    def update_elastic_object(self) -> None:
        """Updates the elastic object if changes occurred."""
        if not self._dirty:
            return

        self._eo.diagonal_mass.setDataValues(
            massDensity=self._material_values['density'])
        self._eo.FEM_force_field.setDataValues(
            youngModulus=[self._material_values['youngs_modulus']]*3,
            # TODO: why multiply????? see Documentation, not Corotational takes Vec instead of float
            poissonRatio=self._material_values['poissons_ratio']
        )

        self._eo.remanence = Tesla.from_T(self._material_values['remanence'])

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
