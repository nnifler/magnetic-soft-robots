"""This module is the main module of the package. It imports all the other modules and classes."""

from .config import Config
from .mesh_loader import MeshLoader
from .scene_builder import SceneBuilder
from .elastic_object import ElasticObject
from .material_loader import MaterialLoader
from .magnetic_controller import MagneticController
from .json_material_manager import JsonMaterialManager
from .analysis_parameters import AnalysisParameters
from .simulation_analyser import SimulationAnalyser, SimulationAnalysisController
