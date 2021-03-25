from .LinkedTransform import LinkedTransform
from kivy.properties import ListProperty
from ui.nodes.ImageSourceView import ImageSourceView
from ui.nodes.ToggleablePreviewView import ToggleablePreviewView
from ui.nodes.CameraSourceView import CameraSourceNode
from ui.nodes.NodeView import NodeView
from typing import List


class TransformationGraph:

    TRANSFORM_TYPES = {
        'image': lambda name: ImageSourceView(name=name),
        'preview': lambda name: ToggleablePreviewView(name=name),
        'camera source': lambda name: CameraSourceNode(name=name)
    }

    camera_resolution = ListProperty([0, 0])

    def __init__(self):
        self.nodes: List[LinkedTransform] = []

    def add(self, transform_type: str, name: str) -> NodeView:
        if self.find_by_name(name) is not None:
            raise ValueError(f'A transform with name {name} already exists')
        if transform_type not in self.__class__.TRANSFORM_TYPES:
            raise ValueError(f'Transform type "{transform_type}" does not exist')
        transform_view = self.__class__.TRANSFORM_TYPES[transform_type](name)
        node_view = NodeView()
        node_view.add_transform_view(transform_view)
        self.nodes.append(transform_view.transform)
        return node_view

    def find_by_name(self, name):
        for node in self.nodes:
            if node.name == name:
                return node
        return None
