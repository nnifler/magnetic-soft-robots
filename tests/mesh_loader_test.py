# ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾ #
#                        MSR, Magnetic Soft Robotics Simulation                        #
#   Copyright (C) 2025 Julius Hahnewald, Heiko Hellkamp, Finn Schubert, Carla Wehner   #
#                                                                                      #
# This program is free software; you can redistribute it and/or                        #
# modify it under the terms of the GNU Lesser General Public                           #
# License as published by the Free Software Foundation; either                         #
# version 2.1 of the License, or (at your option) any later version.                   #
#                                                                                      #
# This program is distributed in the hope that it will be useful,                      #
# but WITHOUT ANY WARRANTY; without even the implied warranty of                       #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU                    #
# Lesser General Public License for more details.                                      #
#                                                                                      #
# You should have received a copy of the GNU Lesser General Public                     #
# License along with this program; if not, write to the Free Software                  #
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301            #
# USA                                                                                  #
# ------------------------------------------------------------------------------------ #
# Contact information: finn.s.schubert@gmail.com                                       #
# ____________________________________________________________________________________ #

"""
This module provides testcases for module src.MeshLoader (US13).
"""
import unittest
from pathlib import Path
import random
import string
from src import MeshLoader
from src.mesh_loader import Mode
from .assets import DummyNode


class TestExceptionalBehavior(unittest.TestCase):
    """
    This testcase tests the exceptional behavior of MeshLoader.
    """

    def test_load_mesh_before_file(self):
        """
        Tests loading a mesh not yet provided.
        """
        uut = MeshLoader()
        root = DummyNode()
        with self.assertRaises(FileNotFoundError):
            uut.load_mesh_into(root, Mode.SURFACE)
        with self.assertRaises(FileNotFoundError):
            uut.load_mesh_into(root, Mode.VOLUMETRIC)

    def test_load_missing_file(self):
        """
        Tests loading a mesh with a wrong path.
        """
        uut = MeshLoader()
        with self.assertRaises(FileNotFoundError):
            uut.load_file(
                Path(
                    'tests/assets/mesh_loader_test/file_that_should_never_be_created.vtk'
                ),
                Mode.SURFACE
            )
        with self.assertRaises(FileNotFoundError):
            uut.load_file(
                Path(
                    'tests/assets/mesh_loader_test/file_that_should_never_be_created.vtk'
                ),
                Mode.VOLUMETRIC
            )

    def test_load_dir_not_file(self):
        """
        Tests loading a mesh with a directory instead of a file.
        """
        uut = MeshLoader()
        with self.assertRaises(FileNotFoundError):
            uut.load_file(
                Path('tests/assets/mesh_loader_test/no_file'), Mode.SURFACE)
        with self.assertRaises(FileNotFoundError):
            uut.load_file(
                Path('tests/assets/mesh_loader_test/no_file'), Mode.VOLUMETRIC)

    def test_load_file_unknown_suffix(self):
        """
        Tests loading a mesh with unknown file extension.
        """
        uut = MeshLoader()
        with self.assertRaises(ValueError):
            uut.load_file(
                Path('tests/assets/mesh_loader_test/file.abcdef'), Mode.SURFACE)
        with self.assertRaises(ValueError):
            uut.load_file(
                Path('tests/assets/mesh_loader_test/file.abcdef'), Mode.VOLUMETRIC)

    def test_load_file_empty(self):
        """
        Tests loading an empty mesh.
        """
        uut = MeshLoader()
        with self.assertRaises(ValueError):
            uut.load_file(
                Path('tests/assets/mesh_loader_test/empty.vtk'), Mode.SURFACE)
        with self.assertRaises(ValueError):
            uut.load_file(
                Path('tests/assets/mesh_loader_test/empty.vtk'), Mode.VOLUMETRIC)

    def test_load_file_wrong_mode(self):
        """
        Tests loading a mesh not compatible with given mode.
        """
        uut = MeshLoader()
        with self.assertRaises(ValueError):
            uut.load_file(
                Path('tests/assets/mesh_loader_test/file.obj'), Mode.VOLUMETRIC)
        with self.assertRaises(ValueError):
            uut.load_file(
                Path('tests/assets/mesh_loader_test/file.stl'), Mode.VOLUMETRIC)


class TestNormalBehavior(unittest.TestCase):
    """
    This testcase tests the normal behavior of MeshLoader.
    """

    def test_load_file_path(self):
        """
        Tests setting path.
        """
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
        """
        Tests loading a mesh into an object and the accessibility of mesh values.
        """
        rand_scaling_factor = random.uniform(0.05, 10)
        uut = MeshLoader(scaling_factor=rand_scaling_factor)
        root = DummyNode()
        path_surface = Path('tests/assets/mesh_loader_test/beam.obj')
        uut.load_file(
            path_surface, Mode.SURFACE)
        uut.load_mesh_into(root, Mode.SURFACE)
        mesh_loader = root.objects['meshLoader_surface']
        self.assertEqual('MeshOBJLoader', mesh_loader['component_type'])
        self.assertEqual(str(path_surface.absolute()), mesh_loader['filename'])
        self.assertEqual([rand_scaling_factor, rand_scaling_factor,
                         rand_scaling_factor], mesh_loader['scale3d'])

        path_volumetric = Path('tests/assets/mesh_loader_test/beam.msh')
        uut.load_file(
            path_volumetric, Mode.VOLUMETRIC)
        uut.load_mesh_into(root, Mode.VOLUMETRIC)
        mesh_loader = root.objects['meshLoader_volumetric']
        self.assertEqual('MeshGmshLoader', mesh_loader['component_type'])
        self.assertEqual(str(path_volumetric.absolute()),
                         mesh_loader['filename'])
        self.assertEqual([rand_scaling_factor, rand_scaling_factor,
                         rand_scaling_factor], mesh_loader['scale3d'])

    def test_reference(self):
        """
        Tests reference method and naming scheme. 
        """
        rand_len_name = random.randint(2, 30)
        rand_name = ''.join(random.sample(
            string.ascii_lowercase*rand_len_name, rand_len_name))
        uut = MeshLoader(rand_name)
        self.assertEqual(f'@{rand_name}_volumetric',
                         uut.reference(Mode.VOLUMETRIC))
        self.assertEqual(f'@{rand_name}_surface', uut.reference(Mode.SURFACE))


def suite() -> unittest.TestSuite:
    """
    Provides MeshLoader tests.
    """
    test_suite = unittest.TestSuite()

    # Insert new tests here
    tests = [
        TestExceptionalBehavior,
        TestNormalBehavior,
    ]

    # Load tests
    loaded_tests = []
    for test in tests:
        loaded_tests.append(unittest.TestLoader().loadTestsFromTestCase(test))

    # Add tests to test suite
    test_suite.addTests(loaded_tests)
    return test_suite
