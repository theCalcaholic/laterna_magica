from kivy.uix.scatter import Scatter
from kivy.properties import StringProperty
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.behaviors.drag import DragBehavior
from kivy.uix.scatter import Scatter
from kivy.graphics import Color, Ellipse
from transforms.LinkedTransform import LinkedTransform
from typing import List, Dict, Tuple, Union


class NodeView(ScatterLayout):

    name = StringProperty('')

    __events__ = ('on_start_connect_nodes', 'on_end_connect_nodes', 'on_connection_established')

    def __init__(self, **kw):
        self.handle_groups: Dict = {}
        self.transform_view: Union[LinkedTransform, None] = None

        def center_in_parent(_, parent):
            print(f'parent: {parent}')
            if parent is not None:
                self.center = parent.center
                self.unbind(parent=center_in_parent)
        self.bind(parent=center_in_parent)

        super().__init__(**kw)

    def on_kv_post(self, base_widget):

        self.handle_groups = {
            'source': self.ids['source_handles'],
            'sink': self.ids['sink_handles'],
        }
        for _, handle_group in self.handle_groups.items():
            handle_group.bind(
                on_start_connect_nodes=lambda _, pos: self.dispatch('on_start_connect_nodes', pos))
            handle_group.bind(
               on_end_connect_nodes=lambda _, handle, touch: self.dispatch('on_end_connect_nodes', handle, touch))
            handle_group.bind(
               on_connection_established=lambda _, *args: self.dispatch('on_connection_established', *args))

    def on_load(self):
        self.center = self.parent.center

    def on_start_connect_nodes(self, pos):
        pass

    def on_end_connect_nodes(self, handle, touch):
        pass

    def on_connection_established(self, handles: Tuple):
        source_node, _ = handles[0].find_node_view_offset()
        sink_node, _ = handles[1].find_node_view_offset()
        source_node.transform_view.transform.attach_sink(sink_node.transform_view.transform)

    def try_connect_nodes(self, handle, pos) -> bool:
        result = False
        for _, handle_group in self.handle_groups.items():
            if handle_group.collide_point(*pos):
                print(handle_group.pos)
                print(pos)
                print(handle.pos)
                print(f'handle_group collision! ({handle_group.connection_type} group)')
                result = result or handle_group.try_connect_nodes(handle,
                                                                  (pos[0] - handle_group.x,
                                                                   pos[1] - handle_group.y))
        return result

    def add_transform_view(self, *l):
        result = self.ids['child_container'].add_widget(*l)
        self.transform_view = l[0]
        self.name = self.transform_view.name
        for channel in self.transform_view.transform.input_channels:
            self.handle_groups['sink'].add_handle()
        for channel in self.transform_view.transform.output_channels:
            self.handle_groups['source'].add_handle()
        return result
