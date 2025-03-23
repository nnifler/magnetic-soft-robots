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
This module provides a dummy node inspired by Sofa.Core.Node.
"""
from typing import Dict


class DummyNode:
    """
    Replaces Sofa.Core.Node for testing purposes
    """

    def __init__(self, name: str = 'root'):
        self.name = name
        self.children = []
        self.objects = dict()

    def addChild(self, name: str):
        """
        Adds a child node to itself.

        :param str name: name of the child node
        :return: the created child node
        """
        self.children.append(DummyNode(name))
        return self.children[-1]

    def addObject(self, component_type: str, **kwargs) -> Dict[str, dict]:
        """
        Adds an object to itself.

        :param str component_type: type of the object to add
        :param dict kwargs: attributes of the object
        :return: the added object
        """
        kwargs['component_type'] = component_type
        if 'name' not in kwargs.keys():
            kwargs['name'] = component_type
        self.objects[kwargs['name']] = kwargs
        return self.objects[kwargs['name']]
