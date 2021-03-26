from kivy.event import EventDispatcher
from kivy.properties import ListProperty, BooleanProperty
from kivy.graphics.texture import Texture
from typing import List, Union, Callable, Set
import numpy as np
import cv2


class LinkedTransform(EventDispatcher):

    __events__ = ('on_frame_received', 'on_frame_processed', 'on_source_attached')

    def __init__(self, name, *args, **kwargs):
        self.name = name
        self._is_active = False
        self._sources: Set[LinkedTransform] = set()
        self._sinks: Set[LinkedTransform] = set()
        self._frame: Union[np.ndarray, None] = None
        self.input_channels = ['image']
        self.output_channels = ['image']
        self.transform_fn: Union[Callable, None] = self.default_transform_fn
        super().__init__(*args, **kwargs)

    def attach_sink(self, sink: 'LinkedTransform'):
        self._sinks.add(sink)
        sink._sources.add(self)
        sink.dispatch('on_source_attached', self)

    def detach_sink(self, sink: 'LinkedTransform'):
        self._sinks.remove(sink)
        sink._sources.remove(self)

    def attach_source(self, source: 'LinkedTransform'):
        self._sources.add(source)
        source._sinks.add(self)
        self.dispatch('on_source_attached', source)

    def detach_source(self, source: 'LinkedTransform'):
        self._sources.remove(source)
        source._sinks.remove(self)

    def place_on_connection(self, source: 'LinkedTransform', sink: 'LinkedTransform'):
        source.detach_sink(sink)
        self.attach_source(source)
        self.attach_sink(sink)

    def receive_frame(self, source: 'LinkedTransform'):
        self.dispatch('on_frame_received', source)
        frames = []
        for s in self._sources:
            frames.append(s.latest_frame)
            if s.latest_frame is None:
                return

        if self.transform_fn is not None and len(self._sources) == len(self.input_channels):
            self._frame = self.transform_fn(*frames)
        elif len(self.input_channels) > 1:
            return

        self.dispatch('on_frame_processed', self)
        for sink in self._sinks:
            sink.receive_frame(self)

    def on_frame_received(self, source: 'LinkedTransform'):
        pass

    def on_frame_processed(self, source: 'LinkedTransform'):
        pass

    def on_source_attached(self, source: 'LinkedTransform'):
        self.receive_frame(source)

    def get_texture(self) -> Union[Texture, None]:
        if self._frame is None:
            return None

        pixels = cv2.flip(cv2.cvtColor(self._frame, cv2.COLOR_BGR2RGB), 0)
        tex = Texture.create(size=(self._frame.shape[1], self._frame.shape[0]), colorfmt='rgb')
        tex.blit_buffer(pixels.tostring(), colorfmt='rgb', bufferfmt='ubyte')
        return tex

    def get_latest_frame(self):
        return self._frame

    def default_transform_fn(self, *frames):
        if len(frames) == 0:
            return self._frame
        else:
            return frames[0]

    texture = property(get_texture)
    latest_frame = property(get_latest_frame)


