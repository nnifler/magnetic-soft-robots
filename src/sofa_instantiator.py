"""This script instantiates the Sofa simulation."""

from pathlib import Path

import Sofa
import Sofa.Gui
import Sofa.Simulation
import SofaRuntime

from src import (Config, SceneBuilder, ElasticObject, MagneticController, StressAnalyzer,
                 MaterialLoader, MeshLoader, SimulationAnalysisController)
from src.mesh_loader import Mode


def main() -> None:
    """Main function that instantiates the Sofa simulation with the given analysis parameters.
    If no analysis parameters are given (i.e `analysis_parameters == None`), 
    the simulation will run without any analysis.
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
        print(f"Model Constraints: {Config.get_constraints()}")
        return

    Config.set_default_plugin_list()

    root = Sofa.Core.Node("root")
    createScene(root)
    Sofa.Simulation.init(root)

    Sofa.Gui.GUIManager.Init("myscene", "qglviewer")
    Sofa.Gui.GUIManager.createGUI(root, __file__)
    Sofa.Gui.GUIManager.SetDimension(1080, 1080)
    Sofa.Gui.GUIManager.MainLoop(root, __file__)
    Sofa.Gui.GUIManager.closeGUI()


# DO NOT REFACTOR TO SNAKE CASE; WILL CRASH SOFA
def createScene(root: Sofa.Core.Node) -> Sofa.Core.Node:
    """Creates the scene for the Sofa simulation with the given argument as the root node
    using the settings specified in the configuration class.

    Args:
        root (Sofa.Core.Node): The root node of the simulation.


    Returns:
        Sofa.Core.Node: The root node of the simulation.
    """
    SceneBuilder(root)

    # can be overwritten / removed as soon as linked to GUI
    mesh_loader = MeshLoader(scaling_factor=Config.get_scale())
    name = Config.get_name()
    mesh_loader.load_file(
        path=Path(__file__).parents[1] / f"lib/models/{name}.msh",
        mode=Mode.VOLUMETRIC,
    )
    mesh_loader.load_file(
        path=Path(__file__).parents[1] / f"lib/models/{name}.stl",
        mode=Mode.SURFACE,
    )

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

    magnetic_controller = MagneticController(elastic_object, mat_loader)
    root.addObject(magnetic_controller)
    analysis_parameter = Config.get_analysis_parameters()
    if analysis_parameter is not None:
        analysis_controller = SimulationAnalysisController(
            root, analysis_parameter)
        root.addObject(analysis_controller)
        root.addObject(
            StressAnalyzer(elastic_object, analysis_parameter)
        )
        if analysis_parameter.stress_analysis:
            analysis_parameter.callpoint.send((
                "stress_reset",
                []
            ))

    return root


# Function used only if this script is called from a python environment
if __name__ == '__main__':
    main()
