from kivy.uix.boxlayout import BoxLayout
from transforms.LinkedTransform import LinkedTransform
from .AbstractTransformNodeView import AbstractTransformNodeView
from .PreviewView import PreviewView
import numpy as np
import cv2


class VideoOverlayView(PreviewView, BoxLayout):

    def __init__(self, **kwargs):
        super().__init__('combine videos', **kwargs)

    def transform_init(self, name):
        super(VideoOverlayView, self).transform_init(name)
        self.transform.input_channels = ['image', 'image']
        self.transform.transform_fn = VideoOverlayView.combine_fn

        # self.transform.bind(on_frame_received=self.on_frame_received)

    # def on_frame_received(self, instance: LinkedTransform, source: LinkedTransform):
        # if len(self.transform._sources) != 2:
        #     return
        # frames = []
        # for s in self.transform._sources:
        #     frames.append(s.latest_frame)
        # if frames[0] is None or frames[1] is None:
        #     return

        # self.transform._frame = self.combine_fn(frames[0], frames[1])
        #self.transform.dispatch('on_frame_processed', self.transform)

    @classmethod
    def combine_fn(cls, frame_0: np.ndarray, frame_1: np.ndarray):
        dimensions_0 = frame_0.shape[:]
        dimensions_1 = frame_1.shape[:]
        offset = (
            max(dimensions_0[0], dimensions_1[0]) - min(dimensions_1[0], dimensions_0[0]),
            max(dimensions_0[1], dimensions_1[1]) - min(dimensions_1[1], dimensions_0[1])
        )

        frame_0_left_bottom = (
            0 if dimensions_0[0] > dimensions_1[0] else int(offset[0] / 2),
            0 if dimensions_0[1] > dimensions_1[1] else int(offset[1] / 2),
        )

        frame_0_right_top = (
            frame_0_left_bottom[0] + dimensions_0[0],
            frame_0_left_bottom[1] + dimensions_0[1]
        )

        frame_1_left_bottom = (
            0 if dimensions_0[0] < dimensions_1[0] else int(offset[0] / 2),
            0 if dimensions_0[1] < dimensions_1[1] else int(offset[1] / 2),
        )

        frame_1_right_top = (
            frame_1_left_bottom[0] + dimensions_1[0],
            frame_1_left_bottom[1] + dimensions_1[1]
        )

        new_shape = [max(dimensions_0[0], dimensions_1[0]), max(dimensions_0[1], dimensions_1[1])]
        new_shape.extend(dimensions_0[2:])
        new_frame = np.zeros(tuple(new_shape), np.uint8)
        # print(new_shape)
        # print(frame_0_left_bottom)
        # print(frame_0_right_top)
        # print(new_frame.shape)
        new_frame[
            frame_0_left_bottom[0]:frame_0_right_top[0],
            frame_0_left_bottom[1]:frame_0_right_top[1]
        ] = frame_0
        new_frame[
            frame_1_left_bottom[0]:frame_1_right_top[0],
            frame_1_left_bottom[1]:frame_1_right_top[1]
        ] = frame_1

        return new_frame


