import os
from src.units.YoungsModulus import YoungsModulus
from src.units.Density import Density
from src import config
from src.mesh_loader import MeshLoader, Mode
from pathlib import Path

class ElasticObject():
    def __init__(self):
        self.node = None
        self.mesh = None
        self.mech_obj = None
        self.volume = None
        self.vertex_forces = None
        self.FEM_force_field = None
        self.diagonal_mass = None
        self.remanence = config.REMANENCE


def createElasticObject(root, name: str, poissonRatio: float, youngsModulus: YoungsModulus, density: Density, scale: float):
    cwd = os.getcwd()
    elastic_object = ElasticObject()

    ## Add Object
    eo_node = root.addChild('object')
    elastic_object.node = eo_node
    eo_node.addObject('EulerImplicitSolver', name="cg_odesolver", rayleighStiffness=0.1, rayleighMass=0.1)
    eo_node.addObject('SparseLDLSolver', name="linear_solver", template="CompressedRowSparseMatrixMat3x3d")

    mesh_loader = MeshLoader(scaling_factor=scale)
    mesh_loader.load_file(path=Path(f"{cwd}/meshes/{name}.msh"), mode=Mode.VOLUMETRIC)
    mesh_loader.load_file(path=Path(f"{cwd}/meshes/{name}.obj"), mode=Mode.SURFACE)
    
    elastic_object.mesh = mesh_loader.load_mesh_into(eo_node, Mode.VOLUMETRIC)
    eo_node.addObject('TetrahedronSetTopologyContainer', name="topo", src=mesh_loader.reference(Mode.VOLUMETRIC))
    elastic_object.mech_obj = eo_node.addObject('MechanicalObject', name="dofs", src=mesh_loader.reference(Mode.VOLUMETRIC))
    eo_node.addObject('TetrahedronSetGeometryAlgorithms', template="Vec3d", name="GeomAlgo")
    elastic_object.diagonal_mass = eo_node.addObject('DiagonalMass', name="Mass", massDensity=density.kgpm3)
    elastic_object.FEM_force_field = eo_node.addObject('TetrahedralCorotationalFEMForceField', template="Vec3d", name="FEM", method="large", poissonRatio=poissonRatio, youngModulus=youngsModulus.Pa, computeGlobalMatrix=False)

    ## Add Constraints
    eo_node.addObject('FixedConstraint', name="FixedConstraint", indices="0 1 2 3")
    eo_node.addObject('LinearSolverConstraintCorrection')

    ## Add Surface
    surf = eo_node.addChild('ExtractSurface')
    surf.addObject('TriangleSetTopologyContainer', name="Container", position="@../topo.position")
    surf.addObject('TriangleSetTopologyModifier', name="Modifier")
    surf.addObject('Tetra2TriangleTopologicalMapping', name="SurfaceExtractMapping", input="@../topo", output="@Container")

    ## Add collision
    collision = surf.addChild('Surf')
    collision.addObject('TriangleSetTopologyContainer', name="Container", src="@../Container")
    collision.addObject('MechanicalObject', name="surfaceDOFs")
    collision.addObject('PointCollisionModel', name="CollisionModel")
    collision.addObject('IdentityMapping', name="CollisionMapping", input="@../../dofs", output="@surfaceDOFs")

    ## Add visuals
    visu = eo_node.addChild("VisualModel")
    visu.loader = mesh_loader.load_mesh_into(visu, Mode.SURFACE)
    visu.addObject('OglModel', name="model", src=mesh_loader.reference(Mode.SURFACE), color=[1., 1., 1.], updateNormals=False)
    visu.addObject('BarycentricMapping')

    l = len(elastic_object.mesh.position.value)
    elastic_object.vertex_forces = [None] * l
    for i in range(l):
        elastic_object.vertex_forces[i] = eo_node.addObject('ConstantForceField', indices = f"{i}", name=f"force_{i}", forces=[0,0,0], showArrowSize="0.001" if config.SHOW_FORCE else "0")

    return elastic_object
