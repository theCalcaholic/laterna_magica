from kivy import require
from kivy.app import App
from .RootWidget import RootWidget
from .MainMenu import MainMenu
from ui.cam_new.NodeEditorView import NodeEditorView
from ui.cam_new.AddTransformDialog import AddTransformDialog
from ui.cam_new.DropDownView import DropDownView
from ui.nodes.DragLabel import DragLabel
from ui.nodes.NodeView import NodeView
from ui.nodes.NodeConnectionHandles import NodeConnectionHandles
from ui.nodes.NodeConnectionHandle import NodeConnectionHandle

require('2.0.0')


class LaternaMagica(App):

    def build(self):
        return RootWidget()
    #     self.root.add_widget(MainMenu())
