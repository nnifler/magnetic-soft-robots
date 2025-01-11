import os
from pathlib import Path

import Sofa.Gui

from src.config2 import Config
from src.SceneBuilder import SceneBuilder
from src.elastic_body import ElasticObject
from src.magnetic_controller import MagneticController
from src.material_loader import MaterialLoader
from src.mesh_loader import MeshLoader, Mode


def main():
    root = Sofa.Core.Node("root")
    createScene(root)
    Sofa.Simulation.init(root)

    Sofa.Gui.GUIManager.Init("myscene", "qglviewer")
    Sofa.Gui.GUIManager.createGUI(root, __file__)
    Sofa.Gui.GUIManager.SetDimension(1080, 1080)
    Sofa.Gui.GUIManager.MainLoop(root)
    Sofa.Gui.GUIManager.closeGUI()


def createScene(root):
    SceneBuilder(root)

    # can be overwritten / removed as soon as linked to GUI
    mesh_loader = MeshLoader(scaling_factor=Config.get_model()["scale"])
    cwd = os.getcwd()
    name = Config.get_model()["name"]
    mesh_loader.load_file(path=Path(f"{cwd}/meshes/{name}.msh"), mode=Mode.VOLUMETRIC)
    mesh_loader.load_file(path=Path(f"{cwd}/meshes/{name}.stl"), mode=Mode.SURFACE)

    elastic_object = ElasticObject(root,
        mesh_loader=mesh_loader,
        poissonRatio=Config.get_material_parameters()["poisson_ratio"],
        youngsModulus=Config.get_material_parameters()["youngs_modulus"],
        density=Config.get_material_parameters()["density"],
    )

    mat_loader = MaterialLoader(elastic_object)

    # can be overwritten / removed as soon as linked to GUI
    mat_loader.set_density(Config.get_material_parameters()["density"])
    mat_loader.set_youngs_modulus(Config.get_material_parameters()["youngs_modulus"])
    mat_loader.set_poissons_ratio(Config.get_material_parameters()["poisson_ratio"])
    mat_loader.set_remanence(Config.get_material_parameters()["remanence"])

    controller = MagneticController(elastic_object, mat_loader)
    root.addObject(controller)

    return root



# Function used only if this script is called from a python environment
if __name__ == '__main__':
    main()
