import unittest
from kivy.event import EventDispatcher
from .LinkedTransform import LinkedTransform
import numpy as np
import cv2
from pathlib import Path


class LinkedTransformMock(LinkedTransform):
    def __init__(self, *args, **kwargs):
        self.received = []
        super().__init__(*args, **kwargs)

    def receive_frame(self, frame: np.ndarray):
        self.received.append(frame)


class SimpleObserver(EventDispatcher):
    pass


class LinkedTransformTest(unittest.TestCase):

    @classmethod
    def get_test_image(cls) -> np.ndarray:
        return cv2.imread(str((Path(__file__).parent.parent / Path('resource/test/Archaeologist-Tux-icon.png'))))

    def test_frames_are_passed_through(self):
        transform_in = LinkedTransform()
        transform_out = LinkedTransformMock()
        transform_in.attach_sink(transform_out)

        frame = LinkedTransformTest.get_test_image()
        transform_in.receive_frame(frame)

        self.assertIn(frame, transform_out.received, 'Transform didn\'t passthrough the frame')

    def test_frame_is_being_transformed(self):
        transform_in = LinkedTransform()
        transform_out = LinkedTransformMock()
        transform_in.attach_sink(transform_out)

        frame = LinkedTransformTest.get_test_image()
        transform_in.transform_fn = np.transpose
        transform_in.receive_frame(frame)

        self.assertTrue((frame.T == transform_out.received).all())

    def test_observer_is_being_notified(self):
        transform_in = LinkedTransform()
        transform_out = LinkedTransformMock()
        transform_in.attach_sink(transform_out)
        results = {'received': False, 'processed': False}

        def register_frame_received(*args):
            results['received'] = True

        def register_frame_processed(*args):
            results['processed'] = True

        transform_in.bind(on_frame_received=register_frame_received, on_frame_processed=register_frame_processed)

        frame = LinkedTransformTest.get_test_image()
        transform_in.receive_frame(frame)

        self.assertTrue(results['received'], 'Observer did not receive "on_frame_received" event')
        self.assertTrue(results['processed'], 'Observer did not receive "on_frame_processed" event')


