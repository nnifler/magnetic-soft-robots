"""This module is responsible for building the scene for the simulation."""

from typing import SupportsFloat
import numpy as np
import Sofa.Core
from . import Config


class SceneBuilder():
    """This class is responsible for building the scene for the simulation."""

    def __init__(self, root: Sofa.Core.Node, gravity_vec: np.ndarray = Config.get_gravity_vec(),
                 dt: float = 0.005) -> None:
        """Initializes the SceneBuilder object.

        Args:
            root (Sofa.Core.Node): The root node of the scene.
            gravity_vec (np.ndarray, optional): The gravity vector. Defaults to Config.get_gravity_vec().
            dt (float, optional): The time difference between each simulation step. Defaults to 0.005.

        Raises:
            ValueError: If dt is not positive.
            TypeError: If gravity_vec has an illegal argument type for gravity component.
            ValueError: If gravity_vec has an invalid length.
        """
        self.root = root

        if dt <= 0:
            raise ValueError("dt must be positive")

        self.root.dt = dt

        for x in gravity_vec:
            if not isinstance(x, SupportsFloat):
                raise TypeError(
                    f"{x} has illegal argument type {type(x)} for gravity component")
        if gravity_vec.shape != (3, ):
            raise ValueError("invalid length for gravity vector")

        self.root.gravity = [0]*3
        if Config.get_use_gravity():
            self.root.gravity = gravity_vec.tolist()
        self._build()

    def _build(self) -> Sofa.Core.Node:
        """Builds the scene for the simulation.

        Returns:
            Sofa.Core.Node: The root node of the scene.
        """
        self._load_plugins()
        if Config.get_show_force():
            self._render_force()
        self._setup_root_simulation()

        if Config.get_show_force():
            for direction in [Config.get_initial_dipole_moment(), Config.get_magnetic_dir()]:
                self._build_reference_direction(direction)

        return self.root

    def create_child(self, name: str) -> Sofa.Core.Node:
        """Creates a child node of the root node.

        Args:
            name (str): The name of the child node.

        Returns:
            Sofa.Core.Node: The child node.
        """
        return self.root.addChild(name)

    def _build_reference_direction(self, direction: np.ndarray):
        """Builds visual representation of the direction.

        Args:
            direction (np.ndarray): The direction of the visual representation.
        """
        ref = self.create_child("reference")
        ref.addObject("MechanicalObject", name="ref")
        ex_dir = direction.tolist()
        ex_dir.append(1)
        ref.addObject('ConstantForceField', forces=direction,
                      showArrowSize="0.01", showColor=ex_dir)
        ref.addObject('VisualStyle', displayFlags="showForceFields")

    def _load_plugins(self):
        """Loads the required SOFA plugins for the simulation."""
        self.root.addObject(
            "RequiredPlugin", pluginName=Config.get_plugin_list())

    def _setup_root_simulation(self):
        """Sets up basic simulation parameters for the root node."""
        self.root.addObject('FreeMotionAnimationLoop')
        self.root.addObject('GenericConstraintSolver',
                            maxIterations=1000, tolerance=1e-6)

        self.root.addObject('CollisionPipeline', name="CollisionPipeline")
        self.root.addObject('BruteForceBroadPhase', name="BroadPhase")
        self.root.addObject('BVHNarrowPhase', name="NarrowPhase")
        self.root.addObject('DefaultContactManager',
                            name="CollisionResponse", response="FrictionContactConstraint")
        self.root.addObject('MinProximityIntersection', useLineLine=True, usePointPoint=True,
                            alarmDistance=0.00003, contactDistance=0.000015, useLinePoint=True)

    def _render_force(self):
        """Adds the force visualization to the scene."""
        self.root.addObject(
            'VisualStyle', displayFlags="showCollisionModels hideVisualModels showForceFields")
