from kivy.uix.boxlayout import BoxLayout
from transforms.LinkedTransform import LinkedTransform
from .AbstractTransformNodeView import AbstractTransformNodeView
import numpy as np


class PreviewView(AbstractTransformNodeView, BoxLayout):

    def transform_init(self, name):
        self.transform = LinkedTransform(name)

    def frame_received(self, instance: LinkedTransform, source: LinkedTransform):
        if 'preview' in self.ids:
            self.ids['preview'].texture = source.texture
