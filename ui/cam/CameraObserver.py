from kivy.uix.camera import Camera
from .ObservableTransform import ObservableTransform


class CameraObserver(Camera):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transform = ObservableTransform()
        self.transform.source = self

    def on_tex(self, *l):
        super(CameraObserver, self).on_tex(*l)



