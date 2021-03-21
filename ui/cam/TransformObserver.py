from kivy.graphics.texture import Texture, TextureRegion
from kivy.properties import ObjectProperty
from kivy.event import EventDispatcher
from typing import Union


class TransformObserver(EventDispatcher):

    _source = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'source' in kwargs:
            self.set_source(kwargs['source'])

    def notify_new_frame(self, texture):
        pass

    def set_source(self, new):
        if self._source is not None:
            self._source.remove(self)
        new.connect(self)
        self._source = new

    def is_active(self) -> bool:
        return self._source is not None

