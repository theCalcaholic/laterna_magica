from transforms.LinkedTransform import LinkedTransform
from .AbstractTransformNodeView import AbstractTransformNodeView
import numpy as np


class VideoPreviewView(AbstractTransformNodeView):

    def transform_init(self, name):
        self.transform = LinkedTransform(name)

    def frame_received(self, transform: LinkedTransform, frame: np.ndarray):
        self.ids['preview'].texture = transform.texture
