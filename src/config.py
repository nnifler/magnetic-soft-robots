from numpy import float32
from src.units.YoungsModulus import YoungsModulus
from src.units.Density import Density

# Choose Parameters
USE_GUI = True
USE_GRAVITY = True
GRAVITY_VEC = [0, float(-10), 0]
NAME = "beam"

## Silicone rubber
POISSON_RATIO = 0.47
YOUNGS_MODULUS = YoungsModulus.fromGPa(0.001)
DENSITY = Density.fromMgpm3(1.1)
MAGNETIC_FORCE = 0.5
REMANENCE = 0.35

MATERIAL_LIST = [
    (0.47, YoungsModulus.fromGPa(0.001), Density.fromMgpm3(1.1), 0.5),   # Silicone Rubber
    (0.4999, YoungsModulus.fromGPa(0.05), Density.fromgpcm3(1.5), 0.5),  # Rubber
    (0.4, YoungsModulus.fromGPa(0.228), Density.fromgpcm3(0.925), 100),  # Low Density Polyethylene
    (0.337, YoungsModulus.fromGPa(3.14), Density.fromgpcm3(1.63), 100)   # PET
]

POISSON_RATIO, YOUNGS_MODULUS, DENSITY, MAGNETIC_FORCE = MATERIAL_LIST[0]

SCALE = 0.02
MAGNETIC_DIR = (0,-1,0)
SHOW_FORCE = True



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
