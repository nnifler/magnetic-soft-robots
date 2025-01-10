import unittest
from src.mesh_loader import MeshLoader, Mode
from tests.assets.dummy_node import DummyNode
from pathlib import Path
from random import randrange


class TestExceptions(unittest.TestCase):
    def test_load_mesh_before_file(self):  # path == None
        uut = MeshLoader()
        root = DummyNode()
        with self.assertRaises(FileNotFoundError):
            uut.load_mesh_into(root, Mode.SURFACE)
        with self.assertRaises(FileNotFoundError):
            uut.load_mesh_into(root, Mode.VOLUMETRIC)

    def test_load_missing_file(self):
        uut = MeshLoader()
        with self.assertRaises(FileNotFoundError):
            uut.load_file(
                Path('tests/assets/mesh_loader_test/file_that_should_never_be_created.vtk'), Mode.SURFACE)
        with self.assertRaises(FileNotFoundError):
            uut.load_file(
                Path('tests/assets/mesh_loader_test/file_that_should_never_be_created.vtk'), Mode.VOLUMETRIC)

    def test_load_dir_not_file(self):
        uut = MeshLoader()
        with self.assertRaises(FileNotFoundError):
            uut.load_file(
                Path('tests/assets/mesh_loader_test/no_file'), Mode.SURFACE)
        with self.assertRaises(FileNotFoundError):
            uut.load_file(
                Path('tests/assets/mesh_loader_test/no_file'), Mode.VOLUMETRIC)

    def test_load_file_unknown_suffix(self):
        uut = MeshLoader()
        with self.assertRaises(ValueError):
            uut.load_file(
                Path('tests/assets/mesh_loader_test/file.abcdef'), Mode.SURFACE)
        with self.assertRaises(ValueError):
            uut.load_file(
                Path('tests/assets/mesh_loader_test/file.abcdef'), Mode.VOLUMETRIC)

    def test_load_file_empty(self):
        uut = MeshLoader()
        with self.assertRaises(ValueError):
            uut.load_file(
                Path('tests/assets/mesh_loader_test/empty.vtk'), Mode.SURFACE)
        with self.assertRaises(ValueError):
            uut.load_file(
                Path('tests/assets/mesh_loader_test/empty.vtk'), Mode.VOLUMETRIC)

    def test_load_file_wrong_mode(self):
        uut = MeshLoader()
        with self.assertRaises(ValueError):
            uut.load_file(
                Path('tests/assets/mesh_loader_test/file.obj'), Mode.VOLUMETRIC)
        with self.assertRaises(ValueError):
            uut.load_file(
                Path('tests/assets/mesh_loader_test/file.stl'), Mode.VOLUMETRIC)


class TestRegularBehavior(unittest.TestCase):
    def test_load_file_path(self):  # path == None
        uut = MeshLoader()
        uut.load_file(
            Path('tests/assets/mesh_loader_test/beam.msh'), Mode.VOLUMETRIC)
        self.assertEqual(Path(
            'tests/assets/mesh_loader_test/beam.msh'), uut._path[Mode.VOLUMETRIC.value])
        uut.load_file(
            Path('tests/assets/mesh_loader_test/beam.obj'), Mode.SURFACE)
        self.assertEqual(Path(
            'tests/assets/mesh_loader_test/beam.obj'), uut._path[Mode.SURFACE.value])

    def test_load_mesh_into_add_object(self):
        uut = MeshLoader('abcdef', 22.3571)
        root = DummyNode()
        path = Path('tests/assets/mesh_loader_test/beam.obj')
        uut.load_file(
            path, Mode.SURFACE)
        uut.load_mesh_into(root, Mode.SURFACE)
        args = root.objects['abcdef_surface']
        self.assertEqual('MeshOBJLoader', args['component_type'])
        self.assertEqual(str(path.absolute()), args['filename'])
        self.assertEqual([22.3571, 22.3571, 22.3571], args['scale3d'])

    def test_reference(self):
        uut = MeshLoader('abcdef')
        self.assertEqual('@abcdef_volumetric', uut.reference(Mode.VOLUMETRIC))
        self.assertEqual('@abcdef_surface', uut.reference(Mode.SURFACE))


def suite() -> unittest.TestSuite:
    suite = unittest.TestSuite()

    # Insert new tests here
    tests = [
        TestExceptions,
        TestRegularBehavior,
    ]

    # Load tests
    loaded_tests = []
    for test in tests:
        loaded_tests.append(unittest.TestLoader().loadTestsFromTestCase(test))

    # Add tests to test suite
    suite.addTests(loaded_tests)
    return suite
