import os
from src.units.YoungsModulus import YoungsModulus
from src.units.Density import Density
from src import config
import numpy as np

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
    elastic_obj = root.addChild('object')
    elastic_object.node = elastic_obj
    elastic_obj.addObject('EulerImplicitSolver', name="cg_odesolver", rayleighStiffness=0.1, rayleighMass=0.1)
    elastic_obj.addObject('SparseLDLSolver', name="linear_solver", template="CompressedRowSparseMatrixMat3x3d")
    elastic_object.mesh = elastic_obj.addObject('MeshGmshLoader', name="meshLoader", filename=f"{cwd}/meshes/{name}.msh", scale3d=[scale]*3)
    elastic_obj.addObject('TetrahedronSetTopologyContainer', name="topo", src="@meshLoader")
    elastic_object.mech_obj = elastic_obj.addObject('MechanicalObject', name="dofs", src="@meshLoader")
    elastic_obj.addObject('TetrahedronSetGeometryAlgorithms', template="Vec3d", name="GeomAlgo")
    elastic_obj.addObject('DiagonalMass', name="Mass", massDensity=density.kgpm3)
    elastic_obj.addObject('TetrahedralCorotationalFEMForceField', template="Vec3d", name="FEM", method="large", poissonRatio=poissonRatio, youngModulus=youngsModulus.Pa, computeGlobalMatrix=False)

    ## Add Constraints
    positions = elastic_object.mesh.position.value.tolist()
    ind = [i for i in range(len(positions)) if positions[i][0] == 0]
    constraints = " ".join(str(x) for x in ind)
    elastic_obj.addObject('FixedConstraint', name="FixedConstraint", indices=constraints)
    elastic_obj.addObject('LinearSolverConstraintCorrection')

    ## Add Surface
    surf = elastic_obj.addChild('ExtractSurface')
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
    visu = elastic_obj.addChild("VisualModel")
    #visu.loader = visu.addObject('MeshOBJLoader', name="loader", filename=f"{cwd}/meshes/{name}.obj")
    visu.loader = visu.addObject('MeshSTLLoader', name="loader", filename=f"{cwd}/meshes/{name}.stl")
    visu.addObject('OglModel', name="model", src="@loader", scale3d=[scale]*3, color=[1., 1., 1.], updateNormals=False)
    visu.addObject('BarycentricMapping')

    l = len(elastic_object.mesh.position.value)
    elastic_object.vertex_forces = [None] * l
    for i in range(l):
        elastic_object.vertex_forces[i] = elastic_obj.addObject('ConstantForceField', indices = f"{i}", name=f"force_{i}", forces=[0,0,0], showArrowSize="0.001" if config.SHOW_FORCE else "0")

    return elastic_object
