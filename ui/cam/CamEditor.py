from kivy.uix.stacklayout import StackLayout
from kivy.properties import NumericProperty, ObjectProperty
from .ObservableTransform import ObservableTransform
from .TransformObserver import TransformObserver
from .SimpleTransform import SimpleTransform
from .CameraObserver import CameraObserver
from .ObservableCameraTransform import ObservableCameraTransform
from .CameraSource import CameraSource
from ..Icon import Icon
from typing import List


class CamEditor(StackLayout):

    camera_id = NumericProperty(1)
    output_sink = ObjectProperty()

    def __init__(self, **kwargs):
        self.transform_stack: List[ObservableTransform] = []
        super().__init__(**kwargs)

    def on_kv_post(self, base_widget):
        self.bind(output_sink=lambda _, sink: self.set_output_sink(sink))
        self.transform_stack.append(self.ids['camera_source'].__self__)

    def add_transform(self):
        child = SimpleTransform(self.transform_stack[-1])
        self.add_widget(child, index=1)
        if self.output_sink is not None:
            print(self.transform_stack)
            self.transform_stack[-1].remove(self.output_sink)
            self.output_sink.set_source(child.transform)
        self.transform_stack.append(child.transform)
        self.add_widget(Icon('ui/resource/arrow.png'), index=1)

    def set_output_sink(self, sink: TransformObserver):
        print(f'set output sink {sink}')
        if self.output_sink is not None:
            self.transform_stack[-1].remove(self.output_sink)
        self.output_sink = sink

        self.output_sink.set_source(self.transform_stack[-1])


