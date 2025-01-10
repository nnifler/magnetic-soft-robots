
import os
from pathlib import Path

import Sofa
from src.config import *
from src.SceneBuilder import SceneBuilder
from src.elastic_body import ElasticObject
from src.magnetic_controller import MagneticController
from src.material_loader import MaterialLoader
from src.mesh_loader import MeshLoader, Mode


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

    # can be overwritten / removed as soon as linked to GUI
    mesh_loader = MeshLoader(scaling_factor=SCALE)
    cwd = os.getcwd()
    mesh_loader.load_file(path=Path(f"{cwd}/meshes/{NAME}.msh"), mode=Mode.VOLUMETRIC)
    mesh_loader.load_file(path=Path(f"{cwd}/meshes/{NAME}.obj"), mode=Mode.SURFACE)

    elastic_object = ElasticObject(root,
        mesh_loader=mesh_loader,
        poissonRatio=POISSON_RATIO,
        youngsModulus=YOUNGS_MODULUS,
        density=DENSITY,
    )

    mat_loader = MaterialLoader(elastic_object)

    # can be overwritten / removed as soon as linked to GUI
    mat_loader.set_density(DENSITY)
    mat_loader.set_youngs_modulus(YOUNGS_MODULUS)
    mat_loader.set_poissons_ratio(POISSON_RATIO)
    mat_loader.set_remanence(REMANENCE)

    controller = MagneticController(elastic_object, mat_loader)
    root.addObject(controller)

    return root



# Function used only if this script is called from a python environment
if __name__ == '__main__':
    main()
