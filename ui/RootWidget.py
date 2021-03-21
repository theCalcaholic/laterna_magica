from kivy.uix.boxlayout import BoxLayout


class RootWidget(BoxLayout):

    def on_kv_post(self, base_widget):
        self.ids['cam_editor'].set_output_sink(self.ids['vcam'])

