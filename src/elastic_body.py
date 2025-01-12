import os
from src.units.YoungsModulus import YoungsModulus
from src.units.Density import Density
from src import config
from src.mesh_loader import MeshLoader, Mode
from pathlib import Path
import numpy as np

class ElasticObject():
    '''
    Class that holds important parameters for the elastic object - the MSR - that is simulated.
    Upon class initialization, code from 
    '''
    def __init__(self, root, mesh_loader: MeshLoader, poissonRatio: float, youngsModulus: YoungsModulus, density: Density):
        self._mesh_loader = mesh_loader
        self._root = root

        self.node = None
        self.mesh = None
        self.mech_obj = None
        self.volume = None
        self.vertex_forces = None
        self.FEM_force_field = None
        self.diagonal_mass = None
        self.remanence = config.REMANENCE


        ## Add Object
        eo_node = self._root.addChild('object')
        self.node = eo_node
        eo_node.addObject('EulerImplicitSolver', name="cg_odesolver", rayleighStiffness=0.1, rayleighMass=0.1)
        eo_node.addObject('SparseLDLSolver', name="linear_solver", template="CompressedRowSparseMatrixMat3x3d")

        self.mesh = self._mesh_loader.load_mesh_into(eo_node, Mode.VOLUMETRIC)
        eo_node.addObject('TetrahedronSetTopologyContainer', name="topo", src=self._mesh_loader.reference(Mode.VOLUMETRIC))
        self.mech_obj = eo_node.addObject('MechanicalObject', name="dofs", src=self._mesh_loader.reference(Mode.VOLUMETRIC))
        eo_node.addObject('TetrahedronSetGeometryAlgorithms', template="Vec3d", name="GeomAlgo")
        self.diagonal_mass = eo_node.addObject('DiagonalMass', name="Mass", massDensity=density.kgpm3)
        self.FEM_force_field = eo_node.addObject('TetrahedralCorotationalFEMForceField', template="Vec3d", name="FEM", method="large", poissonRatio=poissonRatio, youngModulus=youngsModulus.Pa, computeGlobalMatrix=False)

        ## Add Constraints
        positions = self.mesh.position.value.tolist()
        if config.NAME == "gripper":
            ind = [i for i in range(len(positions)) if positions[i][2] == 0.02]
        elif config.NAME == "beam":
            ind = [i for i in range(len(positions)) if positions[i][0] == 0]
        else:
            ind = []
        constraints = " ".join(str(x) for x in ind)
        visualize_constraints = False
        # If True, forces will be added and displayed on the vertices used as a constraint (use only for debugging)
        if visualize_constraints:
            eo_node.addObject('ConstantForceField', indices = constraints, name=f"force_c", forces=[10,0,0], showArrowSize="0.01")
        eo_node.addObject('FixedConstraint', name="FixedConstraint", indices=constraints)
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
        visu.loader = self._mesh_loader.load_mesh_into(visu, Mode.SURFACE)
        visu.addObject('OglModel', name="model", src=self._mesh_loader.reference(Mode.SURFACE), color=[1., 1., 1.], updateNormals=False)
        visu.addObject('BarycentricMapping')

        l = len(self.mesh.position.value)
        self.vertex_forces = [None] * l
        for i in range(l):
            self.vertex_forces[i] = eo_node.addObject('ConstantForceField', indices = f"{i}", name=f"force_{i}", forces=[0,0,0], showArrowSize="0.001" if config.SHOW_FORCE else "0")

