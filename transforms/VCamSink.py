from kivy.properties import NumericProperty, ObjectProperty
from .LinkedTransform import LinkedTransform
from pyfakewebcam.pyfakewebcam import FakeWebcam
from pathlib import Path
from typing import Union
import asyncio
from concurrent import futures
import cv2


class VCamSink(LinkedTransform):

    vcam_id = NumericProperty(-1)
    resolution = ObjectProperty()

    def __init__(self, name, *args, **kwargs):
        self._vcam: Union[None, FakeWebcam] = None
        self.fps = 25
        self.bind(vcam_id=self.load_vcam)
        self.bind(resolution=self.load_vcam)
        self.running = True
        self.pool = futures.ThreadPoolExecutor()
        self.pool.submit(asyncio.run, self.stream())
        super().__init__(name, *args, **kwargs)
        self.output_channels = []

    def load_vcam(self, *args):

        print(f'Loading vcam {self.vcam_id}')
        if self.vcam_id == -1 or not Path(f'/dev/video{self.vcam_id}').exists():
            print(f"Could not load camera /dev/video/{self.vcam_id}: File does not exist")
            return

        if self.resolution is None:
            print(f"Could not load camera /dev/video/{self.vcam_id}: Did not yet receive a resolution")
            return

        try:
            self._vcam = FakeWebcam(f'/dev/video{self.vcam_id}', *self.resolution)
        except Exception as e:
            print(f"Could not load camera /dev/video/{self.vcam_id} due to an unexpected error: {e}")
            return

        print("virt cam is set up")

    async def stream(self):
        while self.running:
            if self._vcam is not None and len(self._sources) > 0:
                #print('publishing frame')
                frame = cv2.cvtColor(list(self._sources)[0].latest_frame, cv2.COLOR_BGR2RGB)
                self._vcam.schedule_frame(frame)
            await asyncio.sleep(1.0/self.fps)
            #print(f'res: {self.resolution}, vcam_id: {self.vcam_id}, sources: {len(self._sources)}, vcam: {self._vcam}')

    def on_frame_received(self, source: 'LinkedTransform'):
        if source.latest_frame is None:
            return
        self.resolution = source.latest_frame.shape[:2]
