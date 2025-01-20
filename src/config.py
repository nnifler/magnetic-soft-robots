import numpy as np
from typing import List

from src.units.YoungsModulus import YoungsModulus
from src.units.Density import Density
from src.units.Tesla import Tesla

class Config:
    ### SOFA UI ###
    _show_force = True

    ### Model ###
    _name = ""
    _scale = 0.0

    ### External forces ###
    _use_gravity = True
    _gravity_vec = np.array([0,0,0])
    _magnetic_force = 0
    _magnetic_dir = np.array([0,0,0])
    _b_field = np.array([0,0,0])
    _initial_dipole_moment = np.array([0,0,0])

    ### Material parameters ###
    _poisson_ratio = 0.0
    _youngs_modulus = YoungsModulus(0)
    _density = Density(0)
    _remanence = Tesla(0)

    ### Plugins ###
    _plugin_list = [""]

    @classmethod
    def set_show_force(cls, show_force: bool) -> None:
        """
        Set if Sofa should display forces acting on the model during the simulation.

        Arguments:
        - show_force: When True, the simulation will display forces.
        """
        cls._show_force = show_force

    @classmethod
    def get_show_force(cls) -> bool:
        """True if Sofa should display forces acting on the model during the simulation."""
        return cls._show_force

    @classmethod
    def set_model(cls, name: str, scale: float) -> None:
        """
        Set the values important for the model.

        Arguments:
        - name: The name of the model and all necessary mesh files.
        - scale: The scaling factor used in the simulation.
        """
        if scale <= 0:
            raise ValueError("Scale must be positive.")
        cls._name = name
        cls._scale = scale

    @classmethod
    def get_name(cls) -> str:
        """Get the name of the model."""
        return cls._name

    @classmethod
    def get_scale(cls) -> float:
        """Get the scaling factor of the model."""
        return cls._scale

    @classmethod
    def set_external_forces(cls,
                            use_gravity: bool,
                            gravity_vec: np.ndarray,
                            magnetic_force: float,
                            magnetic_dir: np.ndarray,
                            initial_dipole_moment: np.ndarray):
        """
        Set the external forces used in the model.

        Arguments:
        - use_gravity: When True, the simulation will use gravity.
        - gravity_vec: The gravity vector.
        - magnetic_force: The strength of the magnetic field.
        - magnetic_dir: The direction of the magnetic field.
        - initial_dipole_moment: The initial dipole moment all tetrahedrons of the model will have.
        """
        if gravity_vec.shape != (3,):
            raise ValueError("Gravity vector must have shape [x,y,z].")
        if magnetic_force <= 0:
            raise ValueError("Magnetic force must be positive.")
        if magnetic_dir.shape != (3,):
            raise ValueError("Magnetic direction must have shape [x,y,z].")
        if initial_dipole_moment.shape != (3,):
            raise ValueError("Initial dipole moment must have shape [x,y,z].")
        cls._use_gravity = use_gravity
        cls._gravity_vec = gravity_vec
        cls._magnetic_force = magnetic_force
        normalised_magnetic_dir = magnetic_dir / np.linalg.norm(magnetic_dir)
        cls._magnetic_dir = normalised_magnetic_dir
        cls._b_field = magnetic_force * normalised_magnetic_dir
        cls._initial_dipole_moment = initial_dipole_moment

    @classmethod
    def get_use_gravity(cls) -> bool:
        """True if the simulation uses gravity."""
        return cls._use_gravity

    @classmethod
    def get_gravity_vec(cls) -> np.ndarray:
        """Get the gravity vector used in the simulation."""
        return cls._gravity_vec

    @classmethod
    def get_magnetic_force(cls) -> float:
        """Get the strength of the magnetic field."""
        return cls._magnetic_force

    @classmethod
    def get_magnetic_dir(cls) -> np.ndarray:
        """Get the direction of the magnetic field."""
        return cls._magnetic_dir

    @classmethod
    def get_b_field(cls) -> np.ndarray:
        """Get the magnetic field used in the simulation."""
        return cls._b_field

    @classmethod
    def get_initial_dipole_moment(cls) -> np.ndarray:
        """Get the initial dipole moment all tetrahedrons of the model will have."""
        return cls._initial_dipole_moment

    @classmethod
    def set_material_parameters(cls,
                                poisson_ratio: float,
                                youngs_modulus: YoungsModulus,
                                density: Density,
                                remanence: Tesla):
        """
        Set the material parameters of the model.

        Arguments:
        - poisson_ratio: The poisson ratio.
        - youngs_modulus: The youngs modulus.
        - density: The density.
        - remanence: The remanence.
        """
        if poisson_ratio < 0.0 or poisson_ratio >= 0.5:
            raise ValueError("Poisson ratio must be between 0 and 0.5.")
        cls._poisson_ratio = poisson_ratio
        cls._youngs_modulus = youngs_modulus
        cls._density = density
        cls._remanence = remanence

    @classmethod
    def get_poisson_ratio(cls) -> float:
        """Get the poisson ratio of the model."""
        return cls._poisson_ratio

    @classmethod
    def get_youngs_modulus(cls) -> YoungsModulus:
        """Get the youngs modulus of the model."""
        return cls._youngs_modulus

    @classmethod
    def get_density(cls) -> Density:
        """Get the density of the model."""
        return cls._density

    @classmethod
    def get_remanence(cls) -> Tesla:
        """Get the remanence of the model."""
        return cls._remanence

    @classmethod
    def set_plugin_list(cls, plugin_list: List[str]):
        """
        Set the plugins used in the Sofa simulation.

        Arguments:
        - plugin_list: The list of plugins.
        """
        cls._plugin_list = plugin_list

    @classmethod
    def get_plugin_list(cls) -> list:
        """Get the plugins used in the Sofa simulation."""
        return cls._plugin_list