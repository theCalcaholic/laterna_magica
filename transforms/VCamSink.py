from kivy.properties import NumericProperty, ObjectProperty
from .LinkedTransform import LinkedTransform
import pyvirtualcam
from pathlib import Path
import asyncio
from concurrent import futures
import cv2


class VCamSink(LinkedTransform):

    vcam_id = NumericProperty(-1)
    resolution = ObjectProperty()

    __events__ = ('on_stream_stopped', 'on_stream_started')

    def __init__(self, name, *args, **kwargs):
        self.fps = 25.0
        self.bind(vcam_id=self.restart_stream)
        self.bind(resolution=self.restart_stream)
        self.running = False
        self.restart_scheduled = False
        super().__init__(name, *args, **kwargs)
        self.output_channels = []

    def restart_stream(self, *args):

        print(self.vcam_id)
        print(self.resolution)

        if self.vcam_id == -1 or not Path(f'/dev/video{self.vcam_id}').exists():
            print(f"Could not load camera /dev/video/{self.vcam_id}: File does not exist")
            return

        if self.resolution is None:
            print(f"Could not load camera /dev/video/{self.vcam_id}: Did not yet receive a resolution")
            return

        if self.running:
            self.restart_scheduled = True
            self.stop_stream()
        else:
            with futures.ThreadPoolExecutor(max_workers=1) as pool:
                pool.submit(asyncio.run, self.stream())

    def stop_stream(self):

        self.running = False

    async def stream(self):
        self.dispatch('on_stream_started')
        self.running = True
        try:
            print(f'Loading vcam /dev/video{self.vcam_id}')
            cam = pyvirtualcam.Camera(width=self.resolution[0], height=self.resolution[1], fps=self.fps,
                                      device=f'/dev/video{self.vcam_id}')
        except Exception as e:
            print(e)
            raise e
        with cam:
            print(self.running)
            print(len(self._sources))
            while self.running and len(self._sources) > 0:
                frame = cv2.cvtColor(list(self._sources)[0].latest_frame, cv2.COLOR_BGR2RGB)
                cam.send(frame)
                cam.sleep_until_next_frame()
        print('stream terminated')
        self.dispatch('on_stream_stopped')

    def on_frame_received(self, source: 'LinkedTransform'):
        if source.latest_frame is None:
            return
        self.resolution = (source.latest_frame.shape[1], source.latest_frame.shape[0])

    def on_stream_started(self):
        print('stream started')

    def on_stream_stopped(self):
        print('stream stopped')
        if self.restart_scheduled:
            self.restart_scheduled = False
            self.start_stream()
