from kivy.uix.stacklayout import StackLayout
from kivy.properties import NumericProperty, ObjectProperty
from ui.cam import ObservableTransform
from ui.cam import TransformObserver
from ui.cam.TransformView import TransformView
from ui.cam import SimpleTransform
from ui.cam import CameraObserver
from ui.cam import ObservableCamera
from ui.cam import CameraSourceView
from ..Icon import Icon
from typing import List


class CamEditor(StackLayout):

    camera_id = NumericProperty(1)
    output_sink = ObjectProperty()

    def __init__(self, **kwargs):
        self.transform_stack: List[ObservableTransform, None] = []
        super().__init__(**kwargs)

    def on_kv_post(self, base_widget):
        self.bind(output_sink=lambda _, sink: self.set_output_sink(sink))
        self.transform_stack.append(self.ids['camera_source'].camera)

    def add_transform(self):
        self.add_widget(Icon('ui/resource/arrow.png'), index=1)
        child = TransformView(index=len(self.transform_stack))
        child.bind(on_ready=lambda _: child.activate(self))
        self.add_widget(child, index=1)
        self.transform_stack.append(None)

    def register(self, index: int, transform: ObservableTransform):
        self.transform_stack[index] = transform
        if index == len(self.transform_stack) - 1 and self.output_sink is not None:
            self.transform_stack[-2].remove(self.output_sink)
            self.output_sink.set_source(self.transform_stack[-1])
        return self.transform_stack[index - 1]

    def set_output_sink(self, sink: TransformObserver):
        print(f'set output sink {sink}')
        if self.output_sink is not None:
            self.transform_stack[-1].remove(self.output_sink)
        self.output_sink = sink

        self.output_sink.set_source(self.transform_stack[-1])


