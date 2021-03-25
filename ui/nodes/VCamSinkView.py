from kivy.uix.boxlayout import BoxLayout
from .AbstractTransformNodeView import AbstractTransformNodeView
from transforms.VCamSink import VCamSink
from transforms.CameraSource import CameraSource
from v4l2ctl import V4l2Capabilities


class VCamSinkView(AbstractTransformNodeView, BoxLayout):

    def __init__(self, name, **kwargs):
        self.available_cameras = []
        super().__init__(name, **kwargs)

    def transform_init(self, name):
        self.transform = VCamSink(name)
        self.available_cameras = CameraSource.find_available_cameras(V4l2Capabilities.VIDEO_OUTPUT)

    def on_kv_post(self, *args):
        for cam in self.available_cameras:
            self.transform.vcam_id = cam
            if self.transform._vcam is not None:
                break
        self.fill_dropdown()

    def fill_dropdown(self):
        dropdown = self.ids['dropdown']
        dropdown.clear()
        for cam_id in self.available_cameras:
            dropdown.add_option(f'Camera No. {cam_id}', cam_id)
        dropdown.bind(on_select=lambda _, choice: setattr(self.transform, 'vcam_id', choice))