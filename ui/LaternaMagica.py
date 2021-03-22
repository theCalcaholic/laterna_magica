from kivy import require
from kivy.app import App
from .RootWidget import RootWidget
from .MainMenu import MainMenu
from ui.cam.CamEditor import CamEditor as CamEditor
from ui.cam.VCamOutputTransform import VCamOutputTransform
from ui.cam.DropDownView import DropDownView

require('2.0.0')


class LaternaMagica(App):

    def build(self):
        return RootWidget()
    #     self.root.add_widget(MainMenu())
