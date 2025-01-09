from src.elastic_body import createElasticObject
# Required import for python
import Sofa
from src.config import *
from src.SceneBuilder import SceneBuilder
from src.magnetic_controller import MagneticController
from src.material_loader import MaterialLoader


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
    SceneBuilder(root)
    elastic_object = createElasticObject(root, 
                               name=NAME, 
                               poissonRatio=POISSON_RATIO,
                               youngsModulus=YOUNGS_MODULUS, 
                               density=DENSITY,
                               scale=SCALE)
    
    mat_loader = MaterialLoader(elastic_object)
    controller = MagneticController(elastic_object, mat_loader)
    root.addObject(controller)

    return root



# Function used only if this script is called from a python environment
if __name__ == '__main__':
    main()
