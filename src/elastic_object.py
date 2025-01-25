"""This module contains the ElasticObject class,
   which is used to create the elastic object that is simulated in the MSR."""

import Sofa.Core
from . import MeshLoader, Config
from .mesh_loader import Mode
from .units import YoungsModulus, Density


class ElasticObject():
    """Class that holds important parameters for
       the elastic object - the MSR - that is simulated."""

    def __init__(self, root: Sofa.Core.Node, mesh_loader: MeshLoader, poisson_ratio: float,
                 youngs_modulus: YoungsModulus, density: Density) -> None:
        """Initializes the ElasticObject with the given parameters.

        Args:
            root (Sofa.Core.Node): The root node of the scene.
            mesh_loader (MeshLoader): The mesh loader object.
            poisson_ratio (float): The Poisson's ratio of the object.
            youngs_modulus (YoungsModulus): The Young's modulus of the object.
            density (Density): The density of the object.
        """
        self._mesh_loader = mesh_loader
        self._root = root

        self.node = None
        self.mesh = None
        self.mech_obj = None
        self.volume = None
        self.vertex_forces = None
        self.FEM_force_field = None
        self.diagonal_mass = None
        self.remanence = Config.get_remanence()

        # Add Object
        eo_node = self._root.addChild('object')
        self.node = eo_node
        eo_node.addObject('EulerImplicitSolver', name="cg_odesolver",
                          rayleighStiffness=0.1, rayleighMass=0.1)
        eo_node.addObject('SparseLDLSolver', name="linear_solver",
                          template="CompressedRowSparseMatrixMat3x3d")

        self.mesh = self._mesh_loader.load_mesh_into(eo_node, Mode.VOLUMETRIC)
        eo_node.addObject('TetrahedronSetTopologyContainer', name="topo",
                          src=self._mesh_loader.reference(Mode.VOLUMETRIC))
        self.mech_obj = eo_node.addObject(
            'MechanicalObject', name="dofs", src=self._mesh_loader.reference(Mode.VOLUMETRIC))
        eo_node.addObject('TetrahedronSetGeometryAlgorithms',
                          template="Vec3d", name="GeomAlgo")
        self.diagonal_mass = eo_node.addObject(
            'DiagonalMass', name="Mass", massDensity=density.kgpm3)
        self.FEM_force_field = eo_node.addObject(
            # 'TetrahedralCorotationalFEMForceField',
            'TetrahedronFEMForceField',
            template="Vec3d",
            name="FEM",
            method="large",
            poissonRatio=poisson_ratio,
            youngModulus=youngs_modulus.Pa,
            # plasticYieldThreshold = 2e-5,
            # 2e-5 is low value, but proportion is about realistic -> von Mises yield condition
            # plasticMaxThreshold = 2.5e-2, # this is very high,
            # plasticCreep = 0.1, # strain from long term stress
            computeGlobalMatrix=False,
            computeVonMisesStress=0,
            showVonMisesStressPerNode=0,
            showVonMisesStressPerElement=0,
        )

        # Add Constraints
        positions = self.mesh.position.value.tolist()
        ind = [idx for idx, pos in enumerate(positions) if pos[0] == 0]
        constraints = " ".join(str(x) for x in ind)
        eo_node.addObject('FixedConstraint',
                          name="FixedConstraint", indices=constraints)
        eo_node.addObject('LinearSolverConstraintCorrection')

        # Add Surface
        surf = eo_node.addChild('ExtractSurface')
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
        visu = eo_node.addChild("VisualModel")
        visu.loader = self._mesh_loader.load_mesh_into(visu, Mode.SURFACE)
        visu.addObject('OglModel', name="model", src=self._mesh_loader.reference(
            Mode.SURFACE), color=[1., 1., 1.], updateNormals=False)
        visu.addObject('BarycentricMapping')

        l = len(self.mesh.position.value)
        self.vertex_forces = [None] * l
        for i in range(l):
            self.vertex_forces[i] = eo_node.addObject(
                'ConstantForceField',
                indices=f"{i}",
                name=f"force_{i}",
                forces=[0, 0, 0],
                showArrowSize="0.001" if Config.get_show_force() else "0"
            )
