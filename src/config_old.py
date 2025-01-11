import numpy as np
from src.units.YoungsModulus import YoungsModulus
from src.units.Density import Density

# SOFA UI Stuff
SHOW_FORCE = False

# Define Model
NAME = "beam" # Name der Mesh Datei rein schreiben
SCALE = 0.02

# External forces
USE_GRAVITY = True
GRAVITY_VEC = np.array([0, float(-9.81), 0]) # GUI? Monderlebnis?
MAGNETIC_FORCE = 0.5 # Interface Regler Werte
MAGNETIC_DIR = np.array([0,-1,0]) # GUI Änderung von Magnetfeldrichtung oben, unten, recht, links
B_FIELD = np.array(MAGNETIC_FORCE * np.array(MAGNETIC_DIR))
INIT = np.array([1, 0, 0]) # Was? How

# Get current Material parameters
POISSON_RATIO = 0.47
YOUNGS_MODULUS = YoungsModulus.fromGPa(0.001)
DENSITY = Density.fromMgpm3(1.1)
REMANENCE = 0.35 # Einheit Teslaaaa, ändern in GUI hehe

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
