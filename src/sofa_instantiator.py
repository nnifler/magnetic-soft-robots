from elastic_body import createElasticObject
# Required import for python
import Sofa


# Choose Parameters
USE_GUI = True
USE_GRAVITY = True
NAME = "beam"
POISSON_RATIO = 0.47 # Ratio halt
YOUNG_MODULUS = 1000000 # Pascal
DENSITY = 1100 # kg/m^3
SCALE = 0.02 # Factor to model
MAGNETIC_FORCE = 0.1 # Newton
MAGNETIC_DIR = (0,1,0)
SHOW_FORCE = False


def main():
    import SofaRuntime
    import Sofa.Gui

    root = Sofa.Core.Node("root")
    createScene(root)
    Sofa.Simulation.init(root)

    if not USE_GUI:
        for iteration in range(10):
            Sofa.Simulation.animate(root, root.dt.value)
    else:
        Sofa.Gui.GUIManager.Init("myscene", "qglviewer")
        Sofa.Gui.GUIManager.createGUI(root, __file__)
        Sofa.Gui.GUIManager.SetDimension(1080, 1080)
        Sofa.Gui.GUIManager.MainLoop(root)
        Sofa.Gui.GUIManager.closeGUI()


def createScene(root):
    root.gravity=[0, -9.81 if USE_GRAVITY else 0, 0]
    root.dt=0.005

    root.addObject("RequiredPlugin", pluginName=[
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

    if SHOW_FORCE:
        root.addObject('VisualStyle', displayFlags="showCollisionModels hideVisualModels showForceFields")

    root.addObject('FreeMotionAnimationLoop')
    root.addObject('GenericConstraintSolver', maxIterations=1000, tolerance=1e-6)

    root.addObject('CollisionPipeline', name="CollisionPipeline")
    root.addObject('BruteForceBroadPhase', name="BroadPhase")
    root.addObject('BVHNarrowPhase', name="NarrowPhase")
    root.addObject('DefaultContactManager', name="CollisionResponse", response="FrictionContactConstraint")
    root.addObject('MinProximityIntersection', useLineLine=True, usePointPoint=True, alarmDistance=0.3, contactDistance=0.15, useLinePoint=True)

    beam = createElasticObject(root, 
                               name=NAME, 
                               poissonRatio=POISSON_RATIO, 
                               youngModulus=YOUNG_MODULUS, 
                               magneticForce=MAGNETIC_FORCE, 
                               magneticDir=MAGNETIC_DIR, 
                               showForce=SHOW_FORCE, 
                               density=DENSITY,
                               scale=SCALE)
    return root



# Function used only if this script is called from a python environment
if __name__ == '__main__':
    main()
