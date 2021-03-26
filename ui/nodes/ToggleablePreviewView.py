from kivy.properties import BooleanProperty
from kivy.graphics.texture import Texture
from .PreviewView import PreviewView
from transforms.LinkedTransform import LinkedTransform
import numpy as np
from array import array


class ToggleablePreviewView(PreviewView):

    active = BooleanProperty(True)

    def __init__(self, **kwargs):

        super().__init__('preview', **kwargs)

    def on_kv_post(self, *args):
        self.bind(active=self.toggle_preview)
        super(ToggleablePreviewView, self).on_kv_post(*args)

    def frame_received(self, instance: LinkedTransform, source: LinkedTransform):
        if not self.active:
            return
        super(ToggleablePreviewView, self).frame_received(instance, source)

    def toggle_preview(self, *args):
        if self.active and len(self.transform._sources) > 0:
            self.frame_received(self.transform, list(self.transform._sources)[0])
        else:
            preview = self.ids['preview']
            if preview.texture is None:
                return
            preview.texture = Texture.create(size=preview.texture.size)
            size = preview.texture.size[0] * preview.texture.size[1] * 3
            buf = [int(255) for x in range(size)]
            arr = array('B', buf)
            preview.texture.blit_buffer(arr, colorfmt='rgb', bufferfmt='ubyte')
