from kivy.event import EventDispatcher
from transforms.LinkedTransform import LinkedTransform
import numpy as np
from typing import Union


class AbstractTransformNodeView(EventDispatcher):

    def __init__(self, name, **kwargs):
        self.transform: Union[LinkedTransform, None] = None
        self.transform_init(name)
        super().__init__(**kwargs)

    def transform_init(self, name):
        raise NotImplementedError()

    def on_kv_post(self, *args):
        self.transform.bind(on_frame_processed=self.frame_received)

    def frame_received(self, transform: LinkedTransform, frame: np.ndarray):
        pass
