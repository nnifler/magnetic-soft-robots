import Sofa
from config import * 


class SceneBuilder():
    def __init__(self, 
            root,
            gravity_vec = [0, -9.81, 0],
            dt = 0.005,
            ) -> None:
        self.root = root
        self.root.gravity = gravity_vec if USE_GRAVITY else [0]*3
        self.root.dt = dt

        self.__build()


    def __build(self):
        self.__load_plugins()
        if SHOW_FORCE: 
            self.__render_force()
        self.__setup_root_simulation()

        return self.root



    def __load_plugins(self):
        self.root.addObject("RequiredPlugin", pluginName=[
            'Sofa.Component.Collision.Detection.Algorithm',
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
            'Sofa.Component.MechanicalLoad'
            ])


    def __setup_root_simulation(self):
        self.root.addObject('FreeMotionAnimationLoop')
        self.root.addObject('GenericConstraintSolver', maxIterations=1000, tolerance=1e-6)

        self.root.addObject('CollisionPipeline', name="CollisionPipeline")
        self.root.addObject('BruteForceBroadPhase', name="BroadPhase")
        self.root.addObject('BVHNarrowPhase', name="NarrowPhase")
        self.root.addObject('DefaultContactManager', name="CollisionResponse", response="FrictionContactConstraint")
        self.root.addObject('MinProximityIntersection', useLineLine=True, usePointPoint=True, alarmDistance=0.3, contactDistance=0.15, useLinePoint=True)


    def __render_force(self):
        self.root.addObject('VisualStyle', displayFlags="showCollisionModels hideVisualModels showForceFields")


