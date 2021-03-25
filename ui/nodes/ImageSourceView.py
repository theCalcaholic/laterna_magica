from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.properties import StringProperty
from kivy.uix.behaviors.drag import DragBehavior
from kivy.uix.popup import Popup
from .AbstractTransformNodeView import AbstractTransformNodeView
from .PreviewView import PreviewView
from .FileChooserDialog import FileChooserDialog
from transforms.SourceTransform import SourceTransform
import cv2
import os


class ImageSourceView(PreviewView, BoxLayout):
    img_uri = StringProperty(None)

    def __init__(self, name, **kwargs):
        self.img_uri = None
        self._popup = None

        super().__init__(name, **kwargs)

    def transform_init(self, name):
        self.transform = SourceTransform(name)

    def on_kv_post(self, *args):
        super(ImageSourceView, self).on_kv_post()
        button = self.ids['choose_image_button']
        self.remove_widget(button)
        self.add_widget(button)

    def show_filechooser_dialog(self):
        content = FileChooserDialog(load=self.load, cancel=self.cancel_dialog)
        self._popup = Popup(title='Load Image', content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    # def try_load_image(self, uri):
    #     self.img_uri = uri
    #     if os.path.isfile(uri):
    #         self.transform.receive_frame(cv2.imread(uri))

    def load(self, path, selection):
        uri = os.path.join(path, selection[0])
        if os.path.isfile(uri):
            self.transform._frame = cv2.imread(uri)
            self.transform.receive_frame(self.transform)
        self._popup.dismiss()

    def cancel_dialog(self):
        self._popup.dismiss()

