from kivy import require
from kivy.app import App
from .RootWidget import RootWidget
from .MainMenu import MainMenu
from .cam.CamEditor import CamEditor as CamEditor
from .cam.VCamOutputTransform import VCamOutputTransform

require('2.0.0')


class LaternaMagica(App):

    def build(self):
        return RootWidget()
    #     self.root.add_widget(MainMenu())
