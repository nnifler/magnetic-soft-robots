from typing import Dict


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


class DummyNode:
    """
    Replaces Sofa.Core.Node for testing purposes
    """

    def __init__(self, name: str = 'root'):
        self.name = name
        self.children = []
        self.objects = dict()

    def addChild(self, name: str):
        self.children.append(DummyNode(name))
        return self.children[-1]

    def addObject(self, component_type: str, **kwargs) -> Dict[str, dict]:
        kwargs['component_type'] = component_type
        if 'name' not in kwargs.keys():
            kwargs['name'] = component_type
        self.objects[kwargs['name']] = kwargs
        # return AttrDict(*self.objects[kwargs['name']])
