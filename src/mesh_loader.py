from pathlib import Path
from typing import Optional


ending_to_loader = {
    "msh":      'MeshGmshLoader',   
    "off":      'MeshOffLoader',
    "vtk":      'MeshVTKLoader',
    "obj":      'MeshOBJLoader',
    "stl":      'MeshSTLLoader',
}


class MeshLoader():
    """Loads meshes into the Sofa Scene, if provided with a Path"""

    def __init__(self, name: str = "meshLoader", scaling_factor: float = 1.):
        self._path: Optional[Path] = None
        self._name = name
        self._scaling = scaling_factor

    def load_file(self, path: Path):
        """Loads a filepath into loader"""
        #TODO: integrity check for file?

        if not path.is_file():
            raise FileNotFoundError(f"Path {path} does not refer to a valid file")

        if path.suffix not in ending_to_loader.keys():
            raise ValueError(f"""Path {path} refers to a file of format {path.suffix}, which is unkown.
                             Please provide a mesh file in one of the following formats:
                             {", ".join(ending_to_loader.keys())}"""
            )

        with open(path) as f:
            if f.readline() == "":
                raise ValueError(f"File {path} empty! Not a valid mesh")

        self._path = path


    def load_mesh_into(self, node):
        """for modularizing mesh loading code"""

        if self._path is None:
            raise FileNotFoundError("Please call load_file before querying mesh_generation")

        mesh = node.addObject(
            ending_to_loader[self._path.suffix],
            name="meshLoader",
            filename=self._path.absolute(),
            scale3d=[self._scaling]*3,
        )
        return mesh


    @property
    def loader_reference(self) -> str:
        """for referencing the loader in other SOFA objects"""
        return "@"+self._name

