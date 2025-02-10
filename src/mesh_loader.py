"""
This module provides functionality for loading mesh files into a SOFA simulation scene.

It defines the MeshLoader class to handle the loading, validation, and referencing of
both surface and volumetric mesh models. Supported mesh formats are defined and mapped
to appropriate SOFA mesh loaders.

Classes:
    Mode: Enum class defining surface and volumetric mesh modes.
    MeshLoader: Class to load, validate, and reference mesh files in a SOFA scene.
"""

from pathlib import Path
from os.path import getsize
from typing import List, Optional, Tuple, Dict
from enum import Enum
import Sofa.Core

# TODO: remove Mode from here


class Mode(Enum):
    """Enum representing mesh modes for surface and volumetric meshes."""
    SURFACE = 0
    VOLUMETRIC = 1


ending_to_loader: Dict[str, str] = {
    ".msh":      'MeshGmshLoader',
    ".off":      'MeshOffLoader',
    ".vtk":      'MeshVTKLoader',
    ".obj":      'MeshOBJLoader',
    ".stl":      'MeshSTLLoader',
}

endings: List[Tuple[str, ...]] = [('.obj', '.stl', '.vtk', '.off', '.msh'),  # SURFACE
                                  ('.msh', '.off', '.vtk')]  # VOLUMETRIC


class MeshLoader():
    """Loads, validates, and references mesh files in a SOFA scene."""

    def __init__(self, name: str = "meshLoader", scaling_factor: float = 1.) -> None:
        """Initializes the MeshLoader.

        Args:
            name (str, optional): The name of the SOFA loader. Defaults to "meshLoader".
            scaling_factor (float, optional): The scaling factor of the model. Defaults to 1..
        """
        self._path: list = [None, None]
        self._name = name
        self._scaling = scaling_factor

    def load_file(self, path: Path, mode: Mode) -> None:
        """Loads a mesh file into the loader.

        Args:
            path (Path): The path to the mesh file.
            mode (Mode): The mode specifying the type of mesh (surface or volumetric).

        """
        # TODO: integrity check for file?

        self.validate_mesh_file(path, mode)
        self._path[mode.value] = path

    def load_mesh_into(self, node: Sofa.Core.Node, mode: Mode) -> Sofa.Core.Object:
        """Loads the mesh into the given SOFA node.

        Args:
            node (Sofa.Core.Node): The node the mesh loads into.
            mode (Mode): The mode specifying the type of mesh (surface or volumetric).

        Raises:
            FileNotFoundError: If path is not set.
            ValueError: If the mesh file name does not match the expected type.

        Returns:
            Sofa.Core.Object: The loaded mesh object.
        """

        path: Optional[Path] = self._path[mode.value]

        if path is None:
            raise FileNotFoundError(
                "Please call load_file before querying mesh_generation")

        filename = path.stem.lower()
        if mode == self.Mode.SURFACE and "_surface" not in filename:
            raise ValueError(
                f"The file '{path.name}' was not saved as a surface mesh file")
        elif mode == self.Mode.VOLUMETRIC and "_volumetric" not in filename:
            raise ValueError(
                f"The file '{path.name}' was not saved as a volumetric mesh file")

        mesh = node.addObject(
            ending_to_loader[path.suffix],
            name=self._name+"_"+mode.name.lower(),
            filename=str(path.absolute()),
            scale3d=[self._scaling]*3,
        )
        return mesh

    def reference(self, mode: Mode) -> str:
        """Generates a reference string for the mesh loader.

        Args:
            mode (Mode): The mode specifying the type of mesh.

        Returns:
            str: The reference string for the mesh loader.
        """
        return "@"+self._name+"_"+mode.name.lower()

    @classmethod
    def validate_mesh_file(cls, path: Path, mode: Mode) -> None:
        """Validates the mesh file for format, mode, and size.

        Args:
            path (Path): The path to the mesh file.
            mode (Mode): The mode specifying the type of mesh.

        Raises:
            FileNotFoundError:  If the path does not refer to a valid file.
            ValueError: If the file format is unsupported.
            ValueError: If the file is empty.
            ValueError: If the file type does not match the specified mesh mode.
        """

        if not path.is_file():
            raise FileNotFoundError(
                f"Path {path} does not refer to a valid file")

        if path.suffix not in ending_to_loader:
            raise ValueError(
                f"Path {path} refers to a file of format {path.suffix}, which is unkown."
                f"Please provide a mesh file in one of the following formats: "
                f"{','.join(ending_to_loader.keys())}"
            )

        if mode == Mode.SURFACE and path.suffix not in endings[Mode.SURFACE.value]:
            raise ValueError(
                f"Path {path} refers to a file of format {path.suffix}, "
                f"which is used only for volumetric meshes."
                f"Please provide a surface mesh file in one of the following formats: "
                f"{','.join(endings[Mode.SURFACE.value])}"
            )
        elif mode == Mode.VOLUMETRIC and path.suffix not in endings[Mode.VOLUMETRIC.value]:
            raise ValueError(
                f"Path {path} refers to a file of format {path.suffix}, "
                f"which is used only for surface meshes."
                f"Please provide a volumetric mesh file in one of the following formats: "
                f"{','.join(endings[Mode.VOLUMETRIC.value])}"
            )

        if getsize(path) == 0:
            raise ValueError(f"File {path} empty! Not a valid mesh")

    def get_supported_meshes(self, mode: Mode) -> set:
        """Returns supported mesh formats for the given mesh type."""
        return set(endings[mode.value])
