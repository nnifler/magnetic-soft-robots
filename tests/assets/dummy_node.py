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
