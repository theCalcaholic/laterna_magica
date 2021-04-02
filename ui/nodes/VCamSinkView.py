from kivy.uix.boxlayout import BoxLayout
from .AbstractTransformNodeView import AbstractTransformNodeView
from transforms.VCamSink import VCamSink
from transforms.CameraSource import CameraSource
from v4l2ctl import V4l2Capabilities


class VCamSinkView(AbstractTransformNodeView, BoxLayout):

    def __init__(self, **kwargs):
        self.available_cameras = []
        super().__init__('virtual camera sink', **kwargs)

    def transform_init(self, name):
        self.transform = VCamSink(name)
        self.available_cameras = CameraSource.find_available_cameras(capability=V4l2Capabilities.VIDEO_OUTPUT)

    def on_kv_post(self, *args):
        self.transform.vcam_id = self.available_cameras[0]
        self.fill_dropdown()

    def fill_dropdown(self):
        dropdown = self.ids['dropdown']
        dropdown.clear()
        for cam_id in self.available_cameras:
            dropdown.add_option(f'Camera No. {cam_id}', cam_id)
        dropdown.bind(on_select=lambda _, choice: setattr(self.transform, 'vcam_id', choice))