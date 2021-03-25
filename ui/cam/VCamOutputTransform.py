from kivy.graphics.texture import Texture, TextureRegion
from kivy.properties import NumericProperty, ObjectProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from .ObservableTransform import ObservableTransform
from .TransformObserver import TransformObserver
from pyfakewebcam import FakeWebcam
from os import path
from pathlib import Path
from typing import Union
import numpy as np
import cv2
import re


class VCamOutputTransform(ObservableTransform, BoxLayout, TransformObserver):
    vcam_id = NumericProperty(defaultvalue=-1)
    resolution = ObjectProperty()

    def __init__(self, *args, **kwargs):
        self.vcam: Union[FakeWebcam, None] = None
        super().__init__(*args, **kwargs)

    def on_kv_post(self, base_widget):
        self.load_vcam()
        self.bind(vcam_id=self.load_vcam)
        self.bind(resolution=self.load_vcam)
        self.preview = self.ids['preview']
        self.ids['dropdown'].bind(on_select=lambda _, choice: setattr(self, 'vcam_id', choice))
        self.fill_dropdown_menu()

    def load_vcam(self, *args):

        print(f'Loading vcam {self.vcam_id}')
        if self.vcam_id == -1 or not path.exists(f'/dev/video{self.vcam_id}'):
            return

        if self.resolution is None:
            return

        self.vcam = FakeWebcam(f'/dev/video{self.vcam_id}', *self.resolution)
        print("virt cam is set up")

    def notify_new_frame(self, texture: Union[Texture, TextureRegion]):
        super(VCamOutputTransform, self).notify_new_frame(texture)

        self.on_new_frame(texture)

        if self.resolution != texture.size:
            self.resolution = texture.size

        if self.vcam is not None:
            buf = np.frombuffer(texture.pixels, np.uint8)
            buf = buf.reshape(texture.height, texture.width, 4)
            self.vcam.schedule_frame(cv2.cvtColor(buf, cv2.COLOR_RGBA2RGB))

    def is_active(self) -> bool:
        return self._source is not None

    def fill_dropdown_menu(self):
        dropdown = self.ids['dropdown']
        dropdown.clear()
        dev_path = Path('/dev')
        for file in dev_path.glob("video*"):
            print(f'checking camera {file}')
            cam_id = int(re.match(r'video(\d+)', file.name).group(1))
            dropdown.add_option(f'Camera No. {cam_id}', cam_id)
        dropdown.bind(on_select=lambda _, choice: setattr(self, 'vcam_id', choice))
