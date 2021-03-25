from .LinkedTransform import LinkedTransform
from ui.nodes.AbstractTransformNodeView import AbstractTransformNodeView
from ui.nodes.ImageSourceView import ImageSourceView
from ui.nodes.VideoPreviewView import VideoPreviewView
from ui.nodes.CameraSourceNode import CameraSourceNode
from typing import List


class TransformationGraph:

    TRANSFORM_TYPES = {
        'image': lambda name: ImageSourceView(name),
        'preview': lambda name: VideoPreviewView(name),
        'camera source': lambda name: CameraSourceNode(name)
    }

    def __init__(self):
        self.nodes: List[LinkedTransform] = []

    def add(self, transform_type: str, name: str) -> AbstractTransformNodeView:
        if self.find_by_name(name) is not None:
            raise ValueError(f'A transform with name {name} already exists')
        if transform_type not in self.__class__.TRANSFORM_TYPES:
            raise ValueError(f'Transform type "{transform_type}" does not exist')
        node = self.__class__.TRANSFORM_TYPES[transform_type](name)
        self.nodes.append(node.transform)
        return node

    def find_by_name(self, name):
        for node in self.nodes:
            if node.name == name:
                return node
        return None
