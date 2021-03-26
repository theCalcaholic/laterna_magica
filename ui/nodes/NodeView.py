from kivy.uix.scatter import Scatter
from kivy.properties import StringProperty, AliasProperty
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.behaviors.drag import DragBehavior
from kivy.uix.scatter import Scatter
from kivy.graphics import Color, Ellipse
from .AbstractTransformNodeView import AbstractTransformNodeView
from transforms.LinkedTransform import LinkedTransform
from typing import List, Dict, Tuple, Union


def get_name_ro(instance):
    return instance._name


class NodeView(ScatterLayout):

    __events__ = ('on_start_connect_nodes', 'on_end_connect_nodes', 'on_connection_established')

    name_ro = AliasProperty(get_name_ro, bind=['_name'])
    _name = StringProperty('')

    def __init__(self, **kw):
        self.handle_groups: Dict = {}
        self.transform_view: Union[LinkedTransform, None] = None
        self.name_label = None
        self.name_input = None
        self.child_container = None
        self.transform_view = None

        def center_in_parent(_, parent):
            print(f'parent: {parent}')
            if parent is not None:
                self.center = parent.center
                self.unbind(parent=center_in_parent)
        self.bind(parent=center_in_parent)

        super().__init__(**kw)

    def on_kv_post(self, base_widget):

        self.name_input = self.ids['name_input']
        self.name_label = self.ids['name_label']
        self.child_container = self.ids['child_container']

        self.name_input.bind(focus=self.update_edit_name)
        self.child_container.remove_widget(self.name_input)

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
        result = self.child_container.add_widget(*l)
        self.transform_view = l[0]
        for channel in self.transform_view.transform.input_channels:
            self.handle_groups['sink'].add_handle()
        for channel in self.transform_view.transform.output_channels:
            self.handle_groups['source'].add_handle()
        self.transform_view.bind(name=lambda _, value: setattr(self, '_name', value))
        self._name = self.transform_view.name
        return result

    def update_edit_name(self, name_input, focus):
        if not focus and self.transform_view.name_is_valid(self.name_input.text):
            self.stop_edit_name()

    def stop_edit_name(self):
        child_index = self.child_container.children.index(self.name_input)
        if child_index != -1:
            self.child_container.remove_widget(self.name_input)
            self.child_container.add_widget(self.name_label, child_index)

    def start_edit_name(self):
        child_index = self.child_container.children.index(self.name_label)
        if child_index != -1:
            self.child_container.remove_widget(self.name_label)
            self.child_container.add_widget(self.name_input, child_index)
            self.name_input.focus = True

    def validate_name(self, name):
        is_valid = self.transform_view.name_is_valid(name)
        bg_color = (1, 1, 1, 1) if is_valid else (1, 0.6, 0.6, 1)
        self.name_input.background_color = bg_color
        return is_valid
