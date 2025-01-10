from typing import Dict


class DummyNode:
    """
    Replaces Sofa.Core.Node for testing purposes
    """

    def __init__(self):
        self.children = []
        self.objects = dict()

    def addObject(self, component_type: str, **kwargs) -> Dict[str, dict]:
        kwargs['component_type'] = component_type
        self.objects[kwargs['name']] = kwargs
        return self.objects[kwargs['name']]
