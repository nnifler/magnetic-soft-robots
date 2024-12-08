from numpy import float32
from src.units.YoungsModulus import YoungsModulus
from src.units.Density import Density

# Choose Parameters
USE_GUI = True
USE_GRAVITY = True
GRAVITY_VEC = [0, float(-10), 0]
NAME = "beam"
POISSON_RATIO = 0.47
YOUNGS_MODULUS = YoungsModulus.fromGPa(0.001)
DENSITY = Density.fromMgpm3(1.1)
SCALE = 0.02
MAGNETIC_FORCE = 0.1
MAGNETIC_DIR = (0,-1,0)
SHOW_FORCE = False


### Plugins ### 
PLUGIN_LIST = ['Sofa.Component.Collision.Detection.Algorithm',
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
]
