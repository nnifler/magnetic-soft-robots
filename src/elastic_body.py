import os
from src.units.YoungsModulus import YoungsModulus
from src.units.Density import Density
from src import config
from src.mesh_loader import MeshLoader

class ElasticObject():
    def __init__(self):
        self.node = None
        self.mesh = None
        self.mech_obj = None
        self.volume = None
        self.vertex_forces = None


def createElasticObject(root, name: str, poissonRatio: float, youngsModulus: YoungsModulus, density: Density, scale: float):
    cwd = os.getcwd()
    elastic_object = ElasticObject()

    ## Add Object
    eo_node = root.addChild('object')
    elastic_object.node = eo_node
    eo_node.addObject('EulerImplicitSolver', name="cg_odesolver", rayleighStiffness=0.1, rayleighMass=0.1)
    eo_node.addObject('SparseLDLSolver', name="linear_solver", template="CompressedRowSparseMatrixMat3x3d")

    elastic_object.mesh = eo_node.addObject('MeshGmshLoader', name="meshLoader", filename=f"{cwd}/meshes/{name}.msh", scale3d=[scale]*3)

    eo_node.addObject('TetrahedronSetTopologyContainer', name="topo", src="@meshLoader")
    elastic_object.mech_obj = eo_node.addObject('MechanicalObject', name="dofs", src="@meshLoader")
    eo_node.addObject('TetrahedronSetGeometryAlgorithms', template="Vec3d", name="GeomAlgo")
    eo_node.addObject('DiagonalMass', name="Mass", massDensity=density.kgpm3)
    eo_node.addObject('TetrahedralCorotationalFEMForceField', template="Vec3d", name="FEM", method="large", poissonRatio=poissonRatio, youngModulus=youngsModulus.Pa, computeGlobalMatrix=False)

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
    visu.loader = visu.addObject('MeshOBJLoader', name="loader", filename=f"{cwd}/meshes/{name}.obj")
    visu.addObject('OglModel', name="model", src="@loader", scale3d=[scale]*3, color=[1., 1., 1.], updateNormals=False)
    visu.addObject('BarycentricMapping')

    l = len(elastic_object.mesh.position.value)
    elastic_object.vertex_forces = [None] * l
    for i in range(l):
        elastic_object.vertex_forces[i] = eo_node.addObject('ConstantForceField', indices = f"{i}", name=f"force_{i}", forces=[0,0,0], showArrowSize="0.001" if config.SHOW_FORCE else "0")

    return elastic_object
