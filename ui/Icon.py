from kivy.uix.widget import Widget
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout


class Icon(BoxLayout):
    img_source = StringProperty(None)

    def __init__(self, icon_source: str, **kwargs):
        self.img_source = icon_source
        super().__init__(**kwargs)
