from .LinkedTransform import LinkedTransform
from typing import Union, List
from kivy.core.camera import Camera as CoreCamera
from kivy.graphics.texture import Texture
from kivy.properties import NumericProperty
from kivy.core.camera import CameraBase
import numpy as np


class CameraSource(LinkedTransform):

    camera_index = NumericProperty(defaultvalue=-1)

    __events__ = ('on_camera_loaded',)

    @classmethod
    def find_available_cameras(cls, max_id: int = 20) -> List[int]:
        ids = []
        for cam_id in range(0, max_id):
            cam = cls.load_camera(cam_id)
            if cam is not None:
                ids.append(cam_id)
        return ids

    @classmethod
    def load_camera(cls, index: int, stopped: bool = True) -> Union[CameraBase, None]:
        try:
            return CoreCamera(index=index, stopped=stopped)
        # Broad except clause is necessary, because we can't really discern between different meaningful exceptions
        # (proper exceptions are not implemented by kv_lang.core.camera)
        except:
            pass

        return None

    def __init__(self, *args, **kwargs):
        self._cam: CoreCamera = None
        self.resolution = [0, 0]
        self.frame = None
        self.bind(camera_index=self.on_index)
        super().__init__(*args, **kwargs)

    def on_index(self, instance, index):
        self._cam = None
        if index < 0:
            return
        self._cam = self.__class__.load_camera(index)
        self._cam.bind(on_load=lambda *args: self.dispatch('on_camera_loaded'))
        self._cam.start()
        self._cam.bind(on_texture=self.on_camera_frame)

    def on_camera_frame(self, *args):
        self.frame = np.frombuffer(self._cam.texture.pixels, np.uint8)
        self.receive_frame(self.frame)

    def on_camera_loaded(self):
        if self._cam.texture is not None:
            self.resolution = list(self._cam.texture.size)

    def get_is_active(self) -> bool:
        return self._cam is not None and self._cam.play

    is_active = property(get_is_active)
