from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty
from kivy.uix.behaviors.drag import DragBehavior
from .AbstractTransformNodeView import AbstractTransformNodeView
from .VideoPreviewView import VideoPreviewView
from transforms.LinkedTransform import LinkedTransform
import cv2
import os


class ImageSourceView(VideoPreviewView, BoxLayout):
    img_uri = StringProperty(None)

    def __init__(self, *args, **kwargs):
        self.img_uri = None
        super().__init__(*args, **kwargs)

    def on_kv_post(self, *args):
        super(ImageSourceView, self).on_kv_post()

    def try_load_image(self, uri):
        self.img_uri = uri
        if os.path.isfile(uri):
            self.transform.receive_frame(cv2.imread(uri))
