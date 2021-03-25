from kivy.uix.label import Label
from kivy.uix.behaviors.drag import DragBehavior
from kivy.uix.button import Button
from kivy.properties import BooleanProperty, ObjectProperty
from kivy.uix.layout import Layout
from kivy.core.window import Window
from kivy.graphics import Color, Ellipse
from .NodeView import NodeView
from typing import Union, Tuple, List


class NodeConnectionHandle(Button):

    # is_loose = BooleanProperty(False)
    paired_handle = ObjectProperty()

    __events__ = ('on_connection_established',)

    def __init__(self, conn_type, **kwargs):
        self.connection_type = conn_type
        # self.is_loose = loose
        self.paired_handle: Union[NodeConnectionHandle, None] = None
        super().__init__(**kwargs)

    def on_kv_post(self, base_widget):
        self.bind(paired_handle=self.on_paired)
        # self.bind(parent=self.on_load)
        # self.bind(is_loose=self.check_connection_established)

    # def find_node_editor(self):
    #     parent = self.parent
    #     while not isinstance(parent, NodeEditorView):
    #         if parent is None:
    #             return None
    #         parent = parent.parent
    #     return parent

    def on_load(self, *args):
        pass
        #node_editor = self.find_node_editor()
        # if not self.is_loose and self.paired_handle is None:
        #     self.paired_handle = NodeConnectionHandle(
        #         conn_type='source' if self.connection_type == 'sink' else 'sink',
        #         loose=True)
        #     Window.add_widget(self.paired_handle, 0)
        #     Window.bind(mouse_pos=lambda _, pos: setattr(self.paired_handle, 'center', pos))

    # def on_motion(self, touch):
    #     print('touch up')
    #     self.center = touch.pos
    #     #self.drag_rectangle = (self.x, self.y, self.width, self.height)

    def on_paired(self, *args):
        pass
    #     if self.paired_handle is None:
    #         return
    #     if self.paired_handle.is_loose:
    #         self.paired_handle.bind(is_loose=self.check_connection_established)
    #     else:
    #         self.opacity = 1

    # def check_connection_established(self, *args):
    #     if self.is_loose or self.paired_handle is None or self.paired_handle.is_loose:
    #         return
    #     self.dispatch('on_connection_established')
    #
    # def on_connection_established(self, *args):
    #     self.opacity = 1

    def find_node_view_offset(self) -> Tuple[NodeView, List[int]]:
        pos = [0, 0]
        parent = self.parent
        d = 20
        while parent is not None and not isinstance(parent, NodeView):
            if not isinstance(parent, Layout):
                pos[0] += parent.x
                pos[1] += parent.y
            # with parent.canvas:
            #     Color(20/d, 20/d, 0)
            #     Ellipse(pos=(pos[0] - self.x - d / 2, pos[1] - self.y - d / 2), size=(d, d))
            #     #Ellipse(pos=(0 - d / 2, 0 - d / 2), size=(d, d))
            # print(parent)
            parent = parent.parent
            d = d - 2
        return parent, [0, 0] if parent is None else pos

    def try_connect_nodes(self, other_handle: 'NodeConnectionHandle', pos):
        print(pos)
        # with self.canvas:
        #     Color(1, 1, 0)
        #     Ellipse(pos=(pos[0] - 5, pos[1]-5), size=(10, 10))
        #     Color(0, 0, 1)
        #     Ellipse(pos=(self.x - 5, self.y - 5), size=(10, 10))
        print(f'({self.connection_type} handle)')
        print(f'came from: {other_handle.connection_type} handle')
        if self.collide_point(*pos) and other_handle.connection_type != self.connection_type:
            print('handle collision!')
            self.paired_handle = other_handle
            self.dispatch('on_connection_established',
                          (self, other_handle) if self.connection_type == 'source' else (other_handle, self))

    def on_connection_established(self, handles):
        pass
