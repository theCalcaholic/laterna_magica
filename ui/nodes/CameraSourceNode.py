from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout

from .AbstractTransformNodeView import AbstractTransformNodeView
from transforms.CameraSource import CameraSource


class CameraSourceNode(AbstractTransformNodeView, BoxLayout):

    def __init__(self, name, **kwargs):
        self.available_cameras = []
        super().__init__(name, **kwargs)

    def transform_init(self, name):
        self.transform = CameraSource(name)
        self.available_cameras = CameraSource.find_available_cameras()

    def on_kv_post(self, *args):
        if len(self.available_cameras) > 0:
            self.transform.camera_index = self.available_cameras[0]
            self.fill_cam_dropdown()

    def fill_cam_dropdown(self):
        dropdown = self.ids['dropdown']
        dropdown.clear()
        for cam_id in self.available_cameras:
            dropdown.add_option(f'Camera No. {cam_id}', cam_id)
        dropdown.bind(on_select=lambda _, choice: setattr(self.transform, 'camera_index', choice))
