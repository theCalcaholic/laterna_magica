from typing import Union, List
from kivy.graphics.texture import Texture
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.camera import Camera
from kivy.event import EventDispatcher
from kivy.core.camera import CameraBase
from kivy.core.camera import Camera as CoreCamera
from kivy.properties import NumericProperty
from ui.cam.ObservableTransform import ObservableTransform


# class ObservableCamera(Camera):
#
#     def __init__(self, callback, **kwargs):
#         super().__init__(**kwargs)
#         self.callback = callback
#
#     def on_tex(self, *l):
#         super(ObservableCamera, self).on_tex(*l)
#         self.callback(self.texture)

class CameraLoadingException(Exception):
    pass


class ObservableCamera(ObservableTransform):

    index = NumericProperty(defaultvalue=-1)
    __events__ = ('on_camera_load', 'on_camera_frame')

    def __init__(self, **kwargs):
        self._cam: CoreCamera = None
        self.texture: Union[Texture, None] = None
        self.texture_size = [0, 0]
        super().__init__(**kwargs)
        self.bind(index=self._on_index)

    @classmethod
    def find_available_cameras(cls, max_id: int = 20) -> List[int]:
        ids = []
        for cam_id in range(0, max_id):
            cam = ObservableCamera.load_camera(cam_id)
            if cam is not None:
                ids.append(cam_id)
        return ids

    def _on_index(self, instance, index):
        self._cam = None
        if index < 0:
            return
        self._cam = ObservableCamera.load_camera(index)
        self._cam.bind(on_load=self.on_camera_load)
        self._cam.bind(on_load=lambda *args: self.dispatch('on_camera_load'))
        self._cam.start()
        self._cam.bind(on_texture=self.on_camera_frame)


    def on_camera_frame(self, *args):
        self.on_new_frame(self._cam.texture)

    def on_camera_load(self, *args):
        if self._cam.texture is not None:
            self.texture = self._cam.texture
            self.texture_size = list(self._cam.texture.size)

    def is_active(self) -> bool:
        return self._cam is not None and self._cam.play

    def remove(self, sink):
        super(ObservableCamera, self).remove(sink)
