import Sofa
from typing import List, SupportsFloat
from . import config


class SceneBuilder():
    def __init__(self,
                 root,
                 gravity_vec=config.GRAVITY_VEC,
                 dt=0.005,
                 ) -> None:
        self.root = root
        self.root.dt = dt

        for x in gravity_vec:
            if not isinstance(x, SupportsFloat):
                raise TypeError(
                    f"{x} has illegal argument type {type(x)} for gravity component")
        if not len(gravity_vec) == 3:
            raise ValueError("invalid length for gravity vector")

        self.root.gravity = [0]*3
        if config.USE_GRAVITY:
            self.root.gravity = gravity_vec
        self._build()

    def _build(self):
        self._load_plugins()
        if config.SHOW_FORCE:
            self._render_force()
        self._setup_root_simulation()

        return self.root

    def _load_plugins(self):
        self.root.addObject("RequiredPlugin", pluginName=config.PLUGIN_LIST)

    def _setup_root_simulation(self):
        self.root.addObject('FreeMotionAnimationLoop')
        self.root.addObject('GenericConstraintSolver',
                            maxIterations=1000, tolerance=1e-6)

        self.root.addObject('CollisionPipeline', name="CollisionPipeline")
        self.root.addObject('BruteForceBroadPhase', name="BroadPhase")
        self.root.addObject('BVHNarrowPhase', name="NarrowPhase")
        self.root.addObject('DefaultContactManager',
                            name="CollisionResponse", response="FrictionContactConstraint")
        self.root.addObject('MinProximityIntersection', useLineLine=True, usePointPoint=True,
                            alarmDistance=0.3, contactDistance=0.15, useLinePoint=True)

    def _render_force(self):
        self.root.addObject(
            'VisualStyle', displayFlags="showCollisionModels hideVisualModels showForceFields")
