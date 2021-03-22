from kivy.properties import ListProperty
from kivy.uix.widget import Widget
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from .ObservableTransform import ObservableTransform
from .TransformObserver import TransformObserver
from .ObservableCamera import ObservableCamera
from typing import Union


class CameraSourceView(BoxLayout):

    available_cam_ids = ListProperty()

    def __init__(self, **kwargs):
        self.camera: Union[ObservableCamera, None] = None
        self.available_cam_ids.clear()
        self.available_cam_ids.extend(ObservableCamera.find_available_cameras())
        super().__init__(**kwargs)

    def on_kv_post(self, base_widget):
        self.camera = ObservableCamera()
        # self.camera.bind(on_camera_frame=self.connect_preview)
        self.camera.index = self.available_cam_ids[0]
        self.camera.preview = self.ids['camera_preview']
        self.fill_cam_dropdown()
        self.ids['camera_selection'].select(self.available_cam_ids[0])

    # def connect_preview(self, *args):
    #     if self.camera.texture is not None:
    #         self.ids['camera_preview'].texture = self.camera.

    def fill_cam_dropdown(self):
        dropdown = self.ids['camera_selection']
        dropdown.clear()
        for cam_id in self.available_cam_ids:
            dropdown.add_option(f'Camera No. {cam_id}', cam_id)
        dropdown.bind(on_select=lambda _, choice: setattr(self.camera, 'index', choice))
