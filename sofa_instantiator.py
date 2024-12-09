import SofaRuntime
import Sofa
import Sofa.Gui
from src.elastic_body import createElasticObject
from src import SceneBuilder
from src.config import *


def main():

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
    SceneBuilder(root)
    beam = createElasticObject(root,
                               name=NAME,
                               poissonRatio=POISSON_RATIO,
                               youngsModulus=YOUNGS_MODULUS,
                               magneticForce=MAGNETIC_FORCE,
                               magneticDir=MAGNETIC_DIR,
                               showForce=SHOW_FORCE,
                               density=DENSITY,
                               scale=SCALE)
    return root


# Function used only if this script is called from a python environment
if __name__ == '__main__':
    main()
