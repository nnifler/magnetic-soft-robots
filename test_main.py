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

import unittest
from tests import *

suite = unittest.TestSuite()
test_suites = []

# Add new test suites here
suite.addTests([
    density_test_suite(),
    tesla_test_suite(),
    youngs_modulus_test_suite(),
    config_test_suite(),
    magnetic_controller_test_suite(),
    material_loader_test_suite(),
    mesh_loader_test_suite(),
    scene_builder_test_suite(),
    beam_test_suite(),
    gripper_3_arm_test_suite(),
    gripper_4_arm_test_suite(),
    simple_butterfly_test_suite(),
    butterfly_test_suite(),
    json_material_manager_test_suite(),
    constraints_test_suite(),
    simulation_analyser_test_suite(),
    analysis_parameters_test_suite(),
    stress_test_suite(),
    stress_widget_suite(),
])

runner = unittest.TextTestRunner()
runner.run(suite)
