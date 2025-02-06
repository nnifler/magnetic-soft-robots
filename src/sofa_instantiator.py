"""This script instantiates the Sofa simulation."""

from pathlib import Path

import Sofa.Gui

from src import Config, SceneBuilder, ElasticObject, MagneticController, MaterialLoader, MeshLoader
from src.mesh_loader import Mode


def main() -> Sofa.Core.Node:
    """Main function that instantiates the Sofa simulation.
    """
    debug = False
    if debug:
        print(f"Show force: {Config.get_show_force()}")
        print(f"Name: {Config.get_name()}")
        print(f"Scale: {Config.get_scale()}")
        print(f"Use gravity: {Config.get_use_gravity()}")
        print(f"Gravity vector: {Config.get_gravity_vec()}")
        print(f"Magnetic force: {Config.get_magnetic_force()}")
        print(f"Magnetic direction: {Config.get_magnetic_dir()}")
        print(f"Initial dipole moment: {Config.get_initial_dipole_moment()}")
        print(f"Poisson ratio: {Config.get_poisson_ratio()}")
        print(f"Young's modulus: {Config.get_youngs_modulus()}")
        print(f"Density: {Config.get_density()}")
        print(f"Remanence: {Config.get_remanence()}")
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
                            'Sofa.Component.MechanicalLoad',
                            'Sofa.Component.Engine.Select',
                            'Sofa.GL.Component.Shader',
                            ])

    root = Sofa.Core.Node("root")
    createScene(root)
    print('not yet crashed')
    return root


def start_loop(root: Sofa.Core.Node) -> None:
    """Starts the Sofa simulation loop.

    Args:
        root (Sofa.Core.Node): The Sofa root node.
    """
    Sofa.Simulation.init(root)
    Sofa.Gui.GUIManager.Init("myscene", "qglviewer")
    Sofa.Gui.GUIManager.createGUI(root, __file__)
    Sofa.Gui.GUIManager.SetDimension(1080, 1080)
    Sofa.Gui.GUIManager.MainLoop(root)
    Sofa.Gui.GUIManager.closeGUI()

# DO NOT REFACTOR TO SNAKE CASE; WILL CRASH SOFA


def createScene(root: Sofa.Core.Node) -> Sofa.Core.Node:
    """Creates the scene for the Sofa simulation with the given argument as the root node.

    Args:
        root (Sofa.Core.Node): The root node.

    Returns:
        Sofa.Core.Node: The root node.
    """
    SceneBuilder(root)

    # can be overwritten / removed as soon as linked to GUI
    mesh_loader = MeshLoader(scaling_factor=Config.get_scale())
    name = Config.get_name()
    mesh_loader.load_file(
        path=Path(f"./lib/models/{name}.msh"), mode=Mode.VOLUMETRIC)
    mesh_loader.load_file(
        path=Path(f"./lib/models/{name}.stl"), mode=Mode.SURFACE)

    elastic_object = ElasticObject(root,
                                   mesh_loader=mesh_loader,
                                   poisson_ratio=Config.get_poisson_ratio(),
                                   youngs_modulus=Config.get_youngs_modulus(),
                                   density=Config.get_density(),
                                   )

    mat_loader = MaterialLoader(elastic_object)

    mat_loader.set_density(Config.get_density())
    mat_loader.set_youngs_modulus(Config.get_youngs_modulus())
    mat_loader.set_poissons_ratio(Config.get_poisson_ratio())
    mat_loader.set_remanence(Config.get_remanence())

    controller = MagneticController(elastic_object, mat_loader)
    root.addObject(controller)

    return root


# Function used only if this script is called from a python environment
if __name__ == '__main__':
    main()
