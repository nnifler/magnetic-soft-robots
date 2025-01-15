from pathlib import Path
from typing import Optional
from enum import Enum
import Sofa.Core.Node


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

    def __init__(self, name: str = "meshLoader", scaling_factor: float = 1.) -> None:
        self._path: list = [None, None]
        self._name = name
        self._scaling = scaling_factor

    def load_file(self, path: Path, mode: Mode) -> None:
        """Loads a filepath into loader

        Args:
            path (Path): file that gets loaded
            mode (Mode): mesh type

        Raises:
            FileNotFoundError: if given `path` is no file
            ValueError: if file suffix is unknown
            ValueError: if surface mode is selected but the file is a volumetric mesh
            ValueError: if volumetric mesh is selected but the file is a surface mesh
            ValueError: if the file is empty
        """
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

        with open(path) as f:
            if f.readline() == "":
                raise ValueError(f"File {path} empty! Not a valid mesh")

        self._path[mode.value] = path

    def load_mesh_into(self, node: Sofa.Core.Node, mode: Mode) -> Sofa.Core.Object:
        """Loads mesh into `node`.

        Args:
            node (Sofa.Core.Node): node the mesh loads into
            mode (Mode): mesh type

        Raises:
            FileNotFoundError: path is not set yet

        Returns:
            Sofa.Core.Object: new object created by this method
        """

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
        """References the loader in other SOFA objects

        Args:
            mode (Mode): mesh type

        Returns:
            str: reference string
        """
        return "@"+self._name+"_"+mode.name.lower()
