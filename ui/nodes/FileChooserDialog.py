from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, ListProperty, StringProperty
from pathlib import Path


class FileChooserDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
    path = StringProperty(str(Path.home()))
    filter = ListProperty(['*.png', '*.jpg', '*.jpeg', '*.JPG'])

