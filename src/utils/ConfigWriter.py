# Define close file in GUI main Window
import os


class ConfigWriter():

    def __init__(self,
                 name,
                 gravity_vector,
                 magnetic_force,
                 magnetic_dir,
                 init,
                 poisson_ratio,
                 youngs_modulus,
                 density,
                 remanence):
        self._name = name
        self._gravity_vector = gravity_vector
        self._magnetic_force = magnetic_force
        self._magnetic_dir = magnetic_dir
        self._init = init
        self._poisson_ratio = poisson_ratio
        self._youngs_modulus = youngs_modulus
        self._density = density
        self._remanence = remanence

    def writeConfig(self):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../config.py")
        config = open(path, 'w')

        # Write imports
        config.write("from src.units.YoungsModulus import YoungsModulus\n" +
                     "from src.units.Density import Density")
        config.write("USE_GUI = True\n" +
                     "SHOW_FORCE = False")
        config.write(f"NAME = \"{self._name}\" \n" +
                      "SCALE = 0.02")


        config.close()