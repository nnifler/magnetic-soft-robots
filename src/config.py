from numpy import float32

# Choose Parameters
USE_GUI = True
USE_GRAVITY = True
GRAVITY_VEC = [0, float(-10), 'a']
NAME = "beam"
POISSON_RATIO = 0.45
YOUNG_MODULUS = 10000
MAGNETIC_FORCE = 0
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
