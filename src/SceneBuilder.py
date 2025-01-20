import Sofa.Core
from src.config import Config
from typing import SupportsFloat
import numpy as np

class SceneBuilder():
    def __init__(self, 
            root,
            gravity_vec: np.ndarray = Config.get_gravity_vec(),
            dt: float = 0.005,
            ) -> None:
        self.root = root

        if dt <= 0: raise ValueError("dt must be positive")

        self.root.dt = dt

        for x in gravity_vec: 
            if not isinstance(x, SupportsFloat): raise TypeError(f"{x} has illegal argument type {type(x)} for gravity component")
        if not gravity_vec.shape == (3,): raise ValueError("invalid length for gravity vector")

        self.root.gravity = [0]*3
        if Config.get_use_gravity():
            self.root.gravity = gravity_vec.tolist()
        self._build()

    def _build(self):
        self._load_plugins()
        if Config.get_show_force():
            self._render_force()
        self._setup_root_simulation()

        if Config.get_show_force():
            for dir in [Config.get_initial_dipole_moment(), Config.get_magnetic_dir()]:
                self._build_reference_direction(dir)

        return self.root
    
    def create_child(self, name) -> Sofa.Core.Node:
        """returns a child of root node"""
        return self.root.addChild(name)

    def _build_reference_direction(self, dir: np.ndarray):
        ref = self.create_child("reference")
        ref.addObject("MechanicalObject", name="ref")
        ex_dir = dir.tolist()
        ex_dir.append(1)
        ref.addObject('ConstantForceField', forces=dir, showArrowSize="0.01", showColor=ex_dir)
        ref.addObject('VisualStyle', displayFlags="showForceFields")

    def _load_plugins(self):
        self.root.addObject("RequiredPlugin", pluginName=Config.get_plugin_list())

    def _setup_root_simulation(self):
        self.root.addObject('FreeMotionAnimationLoop')
        self.root.addObject('GenericConstraintSolver', maxIterations=1000, tolerance=1e-6)

        self.root.addObject('CollisionPipeline', name="CollisionPipeline")
        self.root.addObject('BruteForceBroadPhase', name="BroadPhase")
        self.root.addObject('BVHNarrowPhase', name="NarrowPhase")
        self.root.addObject('DefaultContactManager', name="CollisionResponse", response="FrictionContactConstraint")
        self.root.addObject('MinProximityIntersection', useLineLine=True, usePointPoint=True, alarmDistance=0.3, contactDistance=0.15, useLinePoint=True)

    def _render_force(self):
        self.root.addObject('VisualStyle', displayFlags="showCollisionModels hideVisualModels showForceFields")
