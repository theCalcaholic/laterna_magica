from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.camera import Camera
from .ObservableTransform import ObservableTransform


class ObservableCamera(Camera):

    def __init__(self, callback, **kwargs):
        super().__init__(**kwargs)
        self.callback = callback

    def on_tex(self, *l):
        super(ObservableCamera, self).on_tex(*l)
        self.callback(self.texture)


class ObservableCameraTransform(RelativeLayout, ObservableTransform):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cam = None

    def on_kv_post(self, base_widget):
        try:
            self.cam = ObservableCamera(self.on_new_frame, index=0, size_hint=(1, 1),
                                        pos=(self.center_x - self.size[0]/2,
                                             self.center_y - self.size[1]/2))
            self.add_widget(self.cam)
        except Exception as e:
            print(e)
        return

    def is_active(self) -> bool:
        return self.cam is not None and self.cam.play

    def on_new_frame(self, texture_in) -> None:
        super(ObservableCameraTransform, self).on_new_frame(texture_in)

    def remove(self, sink):
        super(ObservableCameraTransform, self).remove(sink)
