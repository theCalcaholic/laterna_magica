from kivy.event import EventDispatcher
from kivy.uix.widget import Widget
from kivy.properties import StringProperty
from transforms.LinkedTransform import LinkedTransform
import numpy as np
from typing import Union


class AbstractTransformNodeView(Widget):

    name = StringProperty()

    def __init__(self, name, **kwargs):
        self.name = name
        assert self.name is not None
        self.transform: Union[LinkedTransform, None] = None
        self.transform_init(self.name)
        super().__init__(**kwargs)

    def transform_init(self, name):
        raise NotImplementedError()

    def on_kv_post(self, *args):
        assert self.name is not None
        self.transform.bind(on_frame_processed=self.frame_received)

    def frame_received(self, instance: LinkedTransform, source: LinkedTransform):
        pass
