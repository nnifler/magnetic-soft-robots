"""This module contains the configuration for the Sofa simulation."""

from typing import List, Tuple
import numpy as np

from .units import YoungsModulus, Density, Tesla


class Config:
    """This class contains the configuration for the Sofa simulation."""
    ### SOFA UI ###
    _show_force = True

    ### Model ###
    _name = ""
    _scale = 1.0
    _use_constraints = False
    _point_a = np.array([0, 0, 0])
    _point_b = np.array([0, 0, 0])

    ### External forces ###
    _use_gravity = True
    _gravity_vec = np.array([0, 0, 0])
    _magnetic_force = Tesla.from_T(.01)
    _magnetic_dir = np.array([1, 0, 0])
    _b_field = np.array([0, 0, 0])
    _initial_dipole_moment = np.array([0, 0, 0])

    ### Material parameters ###
    _poisson_ratio = 0.0
    _youngs_modulus = YoungsModulus(0)
    _density = Density(0)
    _remanence = Tesla(0)

    ### Plugins ###
    _plugin_list = [""]

    @classmethod
    def set_show_force(cls, show_force: bool) -> None:
        """Set if Sofa should display forces acting on the model during the simulation.

        Args:
            show_force (bool): When True, the simulation will display forces.
        """
        cls._show_force = show_force

    @classmethod
    def get_show_force(cls) -> bool:
        """Get the show_force value.

        Returns:
            bool: True if Sofa should display forces acting on the model during the simulation.
        """
        return cls._show_force

    @classmethod
    def set_model(cls, name: str, scale: float) -> None:
        """Set the values important for the model.

        Args:
            name (str): The name of the model and all necessary mesh files.
            scale (float): The scaling factor used in the simulation.

        Raises:
            ValueError: If scale is less than or equal to 0.
        """
        if scale <= 0:
            raise ValueError("Scale must be positive.")
        cls._name = name
        cls._scale = scale

    @classmethod
    def get_name(cls) -> str:
        """Get the name of the model.

        Returns:
            str: The name of the model and all necessary mesh files.
        """
        return cls._name

    @classmethod
    def get_scale(cls) -> float:
        """Get the scaling factor of the model.

        Returns:
            float: The scaling factor used in the simulation.
        """
        return cls._scale

    @classmethod
    def set_external_forces(cls,
                            use_gravity: bool,
                            gravity_vec: np.ndarray,
                            magnetic_force: Tesla,
                            magnetic_dir: np.ndarray,
                            initial_dipole_moment: np.ndarray) -> None:
        """Set the external forces used in the model.

        Args:
            use_gravity (bool): When True, the simulation will use gravity.
            gravity_vec (np.ndarray): The gravity vector.
            magnetic_force (Tesla): The strength of the magnetic field.
            magnetic_dir (np.ndarray): The direction of the magnetic field.
            initial_dipole_moment (np.ndarray): The initial dipole moment all 
            tetrahedrons of the model will have.

        Raises:
            ValueError: If gravity_vec does not have shape (3,).
            ValueError: If magnetic_force is less than or equal to 0.
            ValueError: If magnetic_dir does not have shape (3,).
            ValueError: If initial_dipole_moment does not have shape (3,).
        """
        if gravity_vec.shape != (3,):
            raise ValueError("Gravity vector must have shape [x,y,z].")
        if magnetic_force.T <= 0:
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
        cls._b_field = magnetic_force.T * normalised_magnetic_dir
        cls._initial_dipole_moment = initial_dipole_moment

    @classmethod
    def get_use_gravity(cls) -> bool:
        """Get the use_gravity value.

        Returns:
            bool: When True, the simulation will use gravity.
        """
        return cls._use_gravity

    @classmethod
    def get_gravity_vec(cls) -> np.ndarray:
        """Get the gravity vector used in the simulation.

        Returns:
            np.ndarray: The gravity vector.
        """
        return cls._gravity_vec

    @classmethod
    def get_magnetic_force(cls) -> Tesla:
        """Get the strength of the magnetic field.

        Returns:
            Tesla: The strength of the magnetic field.
        """
        return cls._magnetic_force

    @classmethod
    def get_magnetic_dir(cls) -> np.ndarray:
        """Get the direction of the magnetic field.

        Returns:
            np.ndarray: The direction of the magnetic field.
        """
        return cls._magnetic_dir

    @classmethod
    def get_b_field(cls) -> np.ndarray:
        """Get the magnetic field used in the simulation.

        Returns:
            np.ndarray: The magnetic field.
        """
        return cls._b_field

    @classmethod
    def get_initial_dipole_moment(cls) -> np.ndarray:
        """Get the initial dipole moment all tetrahedrons of the model will have.

        Returns:
            np.ndarray: The initial dipole moment.
        """
        return cls._initial_dipole_moment

    @classmethod
    def set_material_parameters(cls,
                                poisson_ratio: float,
                                youngs_modulus: YoungsModulus,
                                density: Density,
                                remanence: Tesla) -> None:
        """Set the material parameters of the model.

        Args:
            poisson_ratio (float): The poisson ratio.
            youngs_modulus (YoungsModulus): The youngs modulus.
            density (Density): The density.
            remanence (Tesla): The remanence.

        Raises:
            ValueError: If poisson_ratio is less than 0 or greater than or equal to 0.5.
        """
        if poisson_ratio < 0.0 or poisson_ratio >= 0.5:
            raise ValueError("Poisson ratio must be between 0 and 0.5.")
        cls._poisson_ratio = poisson_ratio
        cls._youngs_modulus = youngs_modulus
        cls._density = density
        cls._remanence = remanence

    @classmethod
    def get_poisson_ratio(cls) -> float:
        """Get the poisson ratio of the model.

        Returns:
            float: The poisson ratio.
        """
        return cls._poisson_ratio

    @classmethod
    def get_youngs_modulus(cls) -> YoungsModulus:
        """Get the youngs modulus of the model.

        Returns:
            YoungsModulus: The youngs modulus.
        """
        return cls._youngs_modulus

    @classmethod
    def get_density(cls) -> Density:
        """Get the density of the model.

        Returns:
            Density: The density.
        """
        return cls._density

    @classmethod
    def get_remanence(cls) -> Tesla:
        """Get the remanence of the model.

        Returns:
            Tesla: The remanence.
        """
        return cls._remanence

    @classmethod
    def set_plugin_list(cls, plugin_list: List[str]):
        """Set the plugins used in the Sofa simulation.

        Args:
            plugin_list (List[str]): The list of plugins.
        """
        cls._plugin_list = plugin_list

    @classmethod
    def get_plugin_list(cls) -> List[str]:
        """Get the plugins used in the Sofa simulation.

        Returns:
            List[str]: The list of plugins.
        """
        return cls._plugin_list

    @classmethod
    def set_constraints(cls, point_a: np.ndarray, point_b: np.ndarray):
        """Set the constraints for the model.

        Args:
            point_a (np.ndarray): The minimum point of the bounding box.
            point_b (np.ndarray): The maximum point of the bounding box.

        Raises:
            ValueError: If point_a or point_b does not have shape (3,).
        """
        if point_a.shape != (3,) or point_b.shape != (3,):
            raise ValueError("Points must have shape (3,).")
        cls._use_constraints = True
        cls._point_a = point_a
        cls._point_b = point_b

    @classmethod
    def get_constraints(cls) -> Tuple[np.ndarray, np.ndarray]:
        """Get the constraints for the model.

        Returns:
            Tuple[np.ndarray, np.ndarray]: The minimum and maximum points of the bounding box.
        """
        return cls._point_a, cls._point_b

    @classmethod
    def get_use_constraints(cls) -> bool:
        """Get the use_constraints value.

        Returns:
            bool: True if constraints are used.
        """
        return cls._use_constraints

    @classmethod
    def set_default_constraints(cls) -> None:
        """Set the constraints to the default values.
        """
        cls._use_constraints = True
        if cls.get_name() == "beam":
            cls._point_a = np.array([-0.005, 0, 0])
            cls._point_b = np.array([0.005, 0.05, 0.05])
        elif cls.get_name() == "gripper_3_arm" or cls.get_name() == "gripper_4_arm":
            cls._point_a = np.array([-0.05, -0.05, 0.01])
            cls._point_b = np.array([0.05, 0.05, 0.03])
        elif cls.get_name() == "butterfly" or cls.get_name() == "simple_butterfly":
            cls._point_a = np.array([-0.1, -0.6, -0.2])
            cls._point_b = np.array([0.1, 0.05, 0.1])
        else:
            cls._use_constraints = False
            cls._point_a = np.array([0, 0, 0])
            cls._point_b = np.array([0, 0, 0])

    @classmethod
    def set_test_env(cls) -> None:
        """Set the configuration to values that can be used in the test environment.
        """
        cls.set_show_force(False)
        cls.set_model('', 1)
        cls.set_external_forces(True,
                                np.array([0, -9.81, 0]),
                                Tesla.from_T(50),
                                np.array([0, 0, 1]),
                                np.array([1, 0, 0])
                                )
        cls.set_material_parameters(0.47,
                                    YoungsModulus.from_GPa(0.1),
                                    Density.from_Mgpm3(1.1),
                                    Tesla.from_T(0.35)
                                    )
        cls.set_plugin_list(['Sofa.Component.Collision.Detection.Algorithm',
                             'Sofa.Component.Collision.Detection.Intersection',
                             'Sofa.Component.Collision.Geometry',
                             'Sofa.Component.Collision.Response.Contact',
                             'Sofa.Component.Constraint.Projective',
                             'Sofa.Component.IO.Mesh',
                             'Sofa.Component.LinearSolver.Iterative',
                             'Sofa.Component.Mapping.Linear',
                             'Sofa.Component.Mass',
                             'Sofa.Component.ODESolver.Backward',
                             'Sofa.Component.SolidMechanics.FEM.Elastic',
                             'Sofa.Component.StateContainer',
                             'Sofa.Component.Topology.Container.Dynamic',
                             'Sofa.Component.Visual',
                             'Sofa.GL.Component.Rendering3D',
                             'Sofa.Component.AnimationLoop',
                             'Sofa.Component.LinearSolver.Direct',
                             'Sofa.Component.Constraint.Lagrangian.Correction',
                             'Sofa.Component.Topology.Mapping',
                             'Sofa.Component.MechanicalLoad',
                             'Sofa.Component.Engine.Select',
                             ])

    @classmethod
    def reset(cls) -> None:
        """Reset the configuration to the default values.
        """
        cls.set_show_force(True)
        cls.set_model('', 1)
        cls.set_default_constraints()
        cls.set_external_forces(True, np.zeros(
            3, dtype=int), Tesla.from_T(.01), np.array([1, 0, 0]), np.zeros(3, dtype=int))
        cls.set_material_parameters(0., YoungsModulus(0), Density(0), Tesla(0))
        cls.set_plugin_list([""])
