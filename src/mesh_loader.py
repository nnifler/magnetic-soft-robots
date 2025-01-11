from pathlib import Path
from os.path import getsize
from typing import Optional
from enum import Enum


class Mode(Enum):
    SURFACE = 0
    VOLUMETRIC = 1


ending_to_loader = {
    ".msh":      'MeshGmshLoader',
    ".off":      'MeshOffLoader',
    ".vtk":      'MeshVTKLoader',
    ".obj":      'MeshOBJLoader',
    ".stl":      'MeshSTLLoader',
}

endings = [('.obj', '.stl', '.vtk', '.off', '.msh'),  # SURFACE
           ('.msh', '.off', '.vtk')]  # VOLUMETRIC


class MeshLoader():
    """Loads meshes into the Sofa Scene, if provided with a Path"""

    def __init__(self, name: str = "meshLoader", scaling_factor: float = 1.):
        self._path: list = [None, None]
        self._name = name
        self._scaling = scaling_factor

    def load_file(self, path: Path, mode: Mode):
        """Loads a filepath into loader"""
        # TODO: integrity check for file?

        if not path.is_file():
            raise FileNotFoundError(
                f"Path {path} does not refer to a valid file")

        if path.suffix not in ending_to_loader.keys():
            raise ValueError(f"""Path {path} refers to a file of format {path.suffix}, which is unkown.
                             Please provide a mesh file in one of the following formats:
                             {", ".join(ending_to_loader.keys())}"""
                             )

        # currently all supported formats are supported with surface mesh types
        if mode == Mode.SURFACE and path.suffix not in endings[Mode.SURFACE.value]:
            raise ValueError(f"""Path {path} refers to a file of format {path.suffix}, which is used only for volumetric meshes.
                             Please provide a surface mesh file in one of the following formats:
                             {", ".join(endings[Mode.SURFACE.value])}"""
                             )

        if mode == Mode.VOLUMETRIC and path.suffix not in endings[Mode.VOLUMETRIC.value]:
            raise ValueError(f"""Path {path} refers to a file of format {path.suffix}, which is used only for surface meshes.
                             Please provide a volumetric mesh file in one of the following formats:
                             {", ".join(endings[Mode.VOLUMETRIC.value])}"""
                             )

        with open(path, mode="r+b") as f:
            f.readline()
        
        if getsize(path) == 0:
            raise ValueError(f"File {path} empty! Not a valid mesh")

        self._path[mode.value] = path

    def load_mesh_into(self, node, mode: Mode):
        """for modularizing mesh loading code"""

        path: Optional[Path] = self._path[mode.value]

        if path is None:
            raise FileNotFoundError(
                "Please call load_file before querying mesh_generation")

        mesh = node.addObject(
            ending_to_loader[path.suffix],
            name=self._name+"_"+mode.name.lower(),
            filename=str(path.absolute()),
            scale3d=[self._scaling]*3,
        )
        return mesh

    def reference(self, mode: Mode) -> str:
        """for referencing the loader for meshes of desired mode in other SOFA objects"""
        return "@"+self._name+"_"+mode.name.lower()
