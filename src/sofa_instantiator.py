import os
from pathlib import Path

import Sofa.Gui

from src.config import Config
from src.SceneBuilder import SceneBuilder
from src.elastic_body import ElasticObject
from src.magnetic_controller import MagneticController
from src.material_loader import MaterialLoader
from src.mesh_loader import MeshLoader, Mode


def main():
    debug = False
    if debug:
        print(f"Show force: {Config.get_show_force()}")
        print(f"Model: {Config.get_model()}")
        print(f"External forces: {Config.get_external_forces()}")
        print(f"Material parameters: {Config.get_material_parameters()}")
        return
    
    Config.set_plugin_list(['Sofa.Component.Collision.Detection.Algorithm',
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
