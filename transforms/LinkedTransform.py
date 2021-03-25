from kivy.event import EventDispatcher
from kivy.properties import ListProperty, BooleanProperty
from kivy.graphics.texture import Texture
from typing import List, Union, Callable, Set
import numpy as np
import cv2


class LinkedTransform(EventDispatcher):

    __events__ = ('on_frame_received', 'on_frame_processed')

    def __init__(self, name, *args, **kwargs):
        self.name = name
        self._is_active = False
        self._sources: Set[LinkedTransform] = set()
        self._sinks: Set[LinkedTransform] = set()
        self._frame: Union[np.ndarray, None] = None
        self.transform_fn: Union[Callable, None] = None
        super().__init__(*args, **kwargs)

    def attach_sink(self, sink: 'LinkedTransform'):
        self._sinks.add(sink)
        sink._sources.add(self)

    def detach_sink(self, sink: 'LinkedTransform'):
        self._sinks.remove(sink)
        sink._sources.remove(self)

    def attach_source(self, source: 'LinkedTransform'):
        self._sources.add(source)
        source._sinks.add(self)

    def detach_source(self, source: 'LinkedTransform'):
        self._sources.remove(source)
        source._sinks.remove(self)

    def place_on_connection(self, source: 'LinkedTransform', sink: 'LinkedTransform'):
        source.detach_sink(sink)
        self.attach_source(source)
        self.attach_sink(sink)

    def receive_frame(self, frame: np.ndarray):
        self.dispatch('on_frame_received', frame)
        if self.transform_fn is not None:
            frame = self.transform_fn(frame)

        self._frame = frame

        self.dispatch('on_frame_processed', frame)
        for sink in self._sinks:
            sink.receive_frame(self._frame)

    def on_frame_received(self, frame: np.ndarray):
        pass

    def on_frame_processed(self, frame: np.ndarray):
        pass

    def get_texture(self) -> Union[Texture, None]:
        if self._frame is None:
            return None
        pixels = cv2.flip(self._frame, 0)
        pixels = cv2.cvtColor(pixels, cv2.COLOR_BGR2RGB)
        tex = Texture.create(size=self._frame.shape[:2], colorfmt='rgb')
        tex.blit_buffer(pixels.tostring(), colorfmt='rgb', bufferfmt='ubyte')
        return tex

    texture = property(get_texture)


