from kivy.graphics.texture import Texture, TextureRegion
from kivy.uix.boxlayout import BoxLayout
from .ObservableTransform import ObservableTransform
from .TransformObserver import TransformObserver
from .ObservableCameraTransform import ObservableCameraTransform
from typing import Union


class CameraSource(ObservableTransform, BoxLayout):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.observable_cam: Union[ObservableCameraTransform, None] = None

    def remove(self, sink: TransformObserver):
        self.observable_cam.remove(sink)

    def on_kv_post(self, base_widget):
        self.observable_cam = self.ids['cam']

    def connect(self, sink: TransformObserver):
        self.observable_cam.connect(sink)

    def on_new_frame(self, texture_in: Union[Texture, TextureRegion]) -> None:
        return self.observable_cam.on_new_frame(texture_in)