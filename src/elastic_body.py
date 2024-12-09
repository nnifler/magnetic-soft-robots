import os
from .units import YoungsModulus
from .units import Density


def createElasticObject(root, name: str, poissonRatio: float, youngsModulus: YoungsModulus, magneticForce: float, magneticDir, showForce: bool, density: Density, scale: float):
    cwd = os.getcwd()
    # Add Object
    elastic_obj = root.addChild('object')
    elastic_obj.addObject('EulerImplicitSolver', name="cg_odesolver",
                          rayleighStiffness=0.1, rayleighMass=0.1)
    elastic_obj.addObject('SparseLDLSolver', name="linear_solver",
                          template="CompressedRowSparseMatrixMat3x3d")
    elastic_obj.addObject('MeshGmshLoader', name="meshLoader",
                          filename=f"{cwd}/meshes/{name}.msh", scale3d=[scale]*3)
    elastic_obj.addObject('TetrahedronSetTopologyContainer',
                          name="topo", src="@meshLoader")
    elastic_obj.addObject('MechanicalObject', name="dofs", src="@meshLoader")
    elastic_obj.addObject('TetrahedronSetGeometryAlgorithms',
                          template="Vec3d", name="GeomAlgo")
    elastic_obj.addObject('DiagonalMass', name="Mass",
                          massDensity=density.kgpm3)
    elastic_obj.addObject('TetrahedralCorotationalFEMForceField', template="Vec3d", name="FEM", method="large",
                          poissonRatio=poissonRatio, youngModulus=youngsModulus.Pa, computeGlobalMatrix=False)

    # Add Constraints
    elastic_obj.addObject(
        'FixedConstraint', name="FixedConstraint", indices="0 1 2 3")
    elastic_obj.addObject('LinearSolverConstraintCorrection')

    # Add Magnetic Field
    fx = magneticForce * magneticDir[0]
    fy = magneticForce * magneticDir[1]
    fz = magneticForce * magneticDir[2]
    elastic_obj.addObject('ConstantForceField', name="mag_force",
                          forces=f"{fx} {fy} {fz}", showArrowSize="0.1" if showForce else "0")

    # Add Surface
    surf = elastic_obj.addChild('ExtractSurface')
    surf.addObject('TriangleSetTopologyContainer',
                   name="Container", position="@../topo.position")
    surf.addObject('TriangleSetTopologyModifier', name="Modifier")
    surf.addObject('Tetra2TriangleTopologicalMapping',
                   name="SurfaceExtractMapping", input="@../topo", output="@Container")

    # Add collision
    collision = surf.addChild('Surf')
    collision.addObject('TriangleSetTopologyContainer',
                        name="Container", src="@../Container")
    collision.addObject('MechanicalObject', name="surfaceDOFs")
    collision.addObject('PointCollisionModel', name="CollisionModel")
    collision.addObject('IdentityMapping', name="CollisionMapping",
                        input="@../../dofs", output="@surfaceDOFs")

    # Add visuals
    visu = elastic_obj.addChild("VisualModel")
    visu.loader = visu.addObject(
        'MeshOBJLoader', name="loader", filename=f"{cwd}/meshes/{name}.obj")
    visu.addObject('OglModel', name="model", src="@loader",
                   scale3d=[scale]*3, color=[1., 1., 1.], updateNormals=False)
    visu.addObject('BarycentricMapping')

    return elastic_obj
