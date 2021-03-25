from kivy.properties import ListProperty
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from .NodeConnectionHandle import NodeConnectionHandle
from ui.cam_new.NodeEditorView import NodeEditorView
from typing import Union


class NodeConnectionHandles(BoxLayout):

    floating_handle: Union[Widget, None] = None

    __events__ = ('on_start_connect_nodes', 'on_end_connect_nodes', 'on_connection_established')

    def __init__(self, **kwargs):
        self.handles = []
        self.connection_type = None
        self.connect_nodes_in_progress = False
        super().__init__(**kwargs)

    def on_kv_post(self, base_widget):
        assert self.connection_type is not None

    def add_handle(self) -> bool:
        if self.floating_handle is not None:
            return False
        handle = NodeConnectionHandle(self.connection_type)
        self.handles.append(handle)
        self.add_widget(handle)
        handle.bind(on_press=lambda touch: self.start_connect_nodes(handle, touch))
        handle.bind(on_touch_up=self.end_connect_nodes)
        handle.bind(on_connection_established=lambda *args: self.dispatch('on_connection_established', *args[1:]))
        return True

    # def attempt_connect(self) -> bool:
    #     print('attempt_connect')
    #     if self.floating_handle is None:
    #         return False
    #     floating_handle = NodeConnectionHandles.floating_handle
    #     if self.ids['add_handle_button'].collide_point(*floating_handle.pos):
    #         floating_handle.parent.remove_widget(floating_handle)
    #         self.add_widget(floating_handle, 1)
    #         floating_handle.is_loose = False
    #         NodeConnectionHandles.floating_handle = None
    #     return True

    def start_connect_nodes(self, handle: NodeConnectionHandle, touch):
        if handle.collide_point(*touch.pos):
            self.connect_nodes_in_progress = True
            node_view, pos = handle.find_node_view_offset()
            pos[0] += node_view.x + handle.center_x
            pos[1] += node_view.y + handle.center_y
            self.dispatch('on_start_connect_nodes', pos)

    def end_connect_nodes(self, handle, touch):
        if self.connect_nodes_in_progress:
            self.dispatch('on_end_connect_nodes', handle, touch)
            self.connect_nodes_in_progress = False

    def try_connect_nodes(self, other_handle: NodeConnectionHandle, pos) -> bool:
        result = False
        for handle in self.handles:
            result = result or handle.try_connect_nodes(other_handle, pos)

    def on_start_connect_nodes(self, *args):
        pass

    def on_end_connect_nodes(self, *args):
        pass

    def on_connection_established(self, handles):
        pass
