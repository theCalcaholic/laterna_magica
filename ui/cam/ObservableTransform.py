from kivy.graphics.texture import Texture, TextureRegion
from kivy.event import EventDispatcher
from kivy.properties import ObjectProperty
from kivy.properties import ListProperty
from .TransformObserver import TransformObserver
from typing import List, Union, Callable
from copy import copy


class ObservableTransform(EventDispatcher):

    sinks = ListProperty()
    preview = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sinks: List[TransformObserver] = []
        self.transform_fn: Union[Callable, None] = None

    def connect(self, sink: TransformObserver):
        if sink not in self.sinks:
            self.sinks.append(sink)

    def remove(self, sink: TransformObserver):
        if sink in self.sinks:
            self.sinks.remove(sink)

    def on_new_frame(self, texture_in: Union[Texture, TextureRegion]) -> None:

        if self.transform_fn is None:
            texture_out = texture_in
        else:
            texture_out = self.transform_fn(texture_in.get_region(0, 0, *texture_in.size))

        for sink in self.sinks:
            sink.notify_new_frame(texture_out)

        if self.preview is not None:
            self.preview.texture = texture_out
            self.preview.canvas.ask_update()
