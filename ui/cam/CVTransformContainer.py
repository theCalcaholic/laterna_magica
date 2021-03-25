from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from .TransformObserver import TransformObserver
from .ObservableTransform import ObservableTransform
from kivy.graphics.texture import Texture, TextureRegion
import numpy as np
import cv2
from typing import Callable, Union, Dict
import time


class CVTransformContainer(BoxLayout, TransformObserver):

    selected_transform = StringProperty()

    MAX_FPS = 10

    def __init__(self, **kwargs):
        self.transform_fns: Dict[
            str, Callable[[Union[Texture, TextureRegion]], Union[Texture, TextureRegion]]] = {
            'none': None,
            'cartoon': CVTransformContainer.filter_cartoon,
            'sketch': CVTransformContainer.filter_sketch,
            'sharpen': CVTransformContainer.filter_sharpen
        }
        self.selected_transform = 'none'

        self.transform = ObservableTransform()
        self.t = time.time_ns()
        # self.bind(selected_transform=self.update_transform)
        # self.selected_transform = 'none'

        super().__init__(**kwargs)

    def on_kv_post(self, base_widget):
        super(CVTransformContainer, self).on_kv_post(base_widget)
        self.transform.preview = self.ids['preview']
        self.fill_dropdown()

    def notify_new_frame(self, texture):
        if self.transform_fns[self.selected_transform] is None:
            self.transform.on_new_frame(texture)
            return
        if time.time_ns() - self.t < 1000000000 / CVTransformContainer.MAX_FPS:
            return
        self.t = time.time_ns()
        buf = np.frombuffer(texture.pixels, np.uint8)
        #buf = cv2.resize(buf, texture.size)
        # buf = cv2.flip(buf, 0)
        buf = buf.reshape(texture.height, texture.width, 4)
        #sw_buf = cv2.cvtColor(buf, cv2.COLOR_RGBA2GRAY)
        buf = cv2.flip(cv2.cvtColor(buf, cv2.COLOR_RGBA2RGB), 0)
        filter_buf = self.transform_fns[self.selected_transform](buf)
        # cv2.imshow('debug', sw_buf)
        # cv2.waitKey(0)
        #sw_buf = cv2.imencode('.jpg', sw_buf)[1].tostring()
        tex = Texture.create(size=texture.size, colorfmt='rgb')
        tex.blit_buffer(filter_buf.tostring(), colorfmt='rgb', bufferfmt='ubyte')
        self.transform.on_new_frame(tex)

    def fill_dropdown(self):
        dropdown = self.ids['transform_dropdown']
        dropdown.clear()
        for key in self.transform_fns.keys():
            dropdown.add_option(key, key)
        dropdown.bind(on_select=lambda _, choice: setattr(self, 'selected_transform', choice))

    @classmethod
    def filter_cartoon(cls, buf):
        return cv2.stylization(buf, sigma_s=150, sigma_r=0.25)

    @classmethod
    def filter_sketch(cls, buf):
        return cv2.pencilSketch(buf, sigma_s=60, sigma_r=0.5, shade_factor=0.02)[0]

    @classmethod
    def filter_sharpen(cls, buf):
        sharpen_kernel = np.array(([[0, -1, 0], [-1, 9, -1], [0, -1, 0]]), np.float32) / 9
        return cv2.filter2D(src=buf, kernel=sharpen_kernel, ddepth=-1)