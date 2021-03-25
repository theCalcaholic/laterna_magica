from kivy.uix.scatter import Scatter
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.behaviors.drag import DragBehavior
from kivy.uix.scatter import Scatter
from kivy.graphics import Color, Ellipse
from typing import List


class NodeView(ScatterLayout):

    __events__ = ('on_start_connect_nodes', 'on_end_connect_nodes', 'on_connection_established')

    def __init__(self, **kw):
        self.handle_groups: List = []
        super().__init__(**kw)

    def on_kv_post(self, base_widget):
        for identifier in 'sink_handles', 'source_handles':
            self.handle_groups.append(self.ids[identifier])
        for handle_group in self.handle_groups:
            handle_group.bind(
                on_start_connect_nodes=lambda _, pos: self.dispatch('on_start_connect_nodes', pos))
            handle_group.bind(
               on_end_connect_nodes=lambda _, handle, touch: self.dispatch('on_end_connect_nodes', handle, touch))
            handle_group.bind(
               on_connection_established=lambda _, *args: self.dispatch('on_connection_established', *args))

        for handle in self.handle_groups[1].handles:
            handle.find_node_view_offset()

    def on_start_connect_nodes(self, pos):
        pass

    def on_end_connect_nodes(self, handle, touch):
        pass

    def on_connection_established(self, handle):
        pass

    def try_connect_nodes(self, handle, pos) -> bool:
        result = False
        for handle_group in self.handle_groups:
            if handle_group.collide_point(*pos):
                print(handle_group.pos)
                print(pos)
                print(handle.pos)
                print(f'handle_group collision! ({handle_group.connection_type} group)')
                result = result or handle_group.try_connect_nodes(handle,
                                                                  (pos[0] - handle_group.x,
                                                                   pos[1] - handle_group.y))
        return result

