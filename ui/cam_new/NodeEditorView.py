from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Ellipse, Bezier, Line
from kivy.core.window import Window
from transforms.TransformationGraph import TransformationGraph
from ui.nodes.NodeView import NodeView
from transforms.LinkedTransform import LinkedTransform
from .NodeConnectionData import NodeConnectionData
from typing import List, Union, Set, Dict


class NodeEditorView(FloatLayout):

    def __init__(self, **kwargs):
        self.transform_graph = TransformationGraph()
        self.nodes: List[NodeView] = []
        self.node_connection_in_progress = False
        self.node_connection_start_pos: Union[List, None] = None
        self.line: Union[Line, None] = None
        self.connections: Set[NodeConnectionData] = set()

        super().__init__(**kwargs)

    def on_kv_post(self, base_widget):
        self.ids['add_transform_dialog'].transform_options = self.transform_graph.TRANSFORM_TYPES.keys()
        self.ids['add_transform_dialog'].bind(on_add_transform=self.add_transform)

    def add_transform(self, _, transform_type):
        node = self.transform_graph.add(transform_type)
        self.nodes.append(node)
        self.add_widget(node)
        node.bind(on_start_connect_nodes=self.on_start_connect_nodes)
        node.bind(on_end_connect_nodes=self.on_end_connect_nodes)
        node.bind(on_connection_established=self.on_connection_established)

    def show_add_node_dialog(self, *args):
        print('Showing context menu...')
        self.ids['add_transform_dialog'].show()

    def validate_transform_name(self, name):
        return name != '' and self.transform_graph.find_by_name(name) is None

    def on_start_connect_nodes(self, _, pos):
        self.node_connection_in_progress = True
        self.node_connection_start_pos = pos
        with self.canvas:
            Color(0, 0.6, 0.8)
            self.line = Bezier(points=pos, segments=50, dash_length=20, dash_offset=5)

    def on_touch_move(self, touch):
        if not self.node_connection_in_progress:
            return
        points = self.line.points[:2]
        points.extend([points[0] + ((touch.x - points[0]) / 3), points[1]])
        points.extend([points[0] + (2 * (touch.x - points[0]) / 3), touch.y])
        points.extend(touch.pos)
        self.line.points = points

    def on_end_connect_nodes(self, _, handle, touch):
        print('on_end_connect_nodes')
        self.node_connection_in_progress = False
        node_view, offset = handle.find_node_view_offset()
        offset[0] += node_view.x
        offset[1] += node_view.y
        pos = touch.pos[0] + offset[0], touch.pos[1] + offset[1]
        # with self.canvas:
        #     Color(1, 0, 0)
        #     Ellipse(pos=(pos[0] - 20 / 2, pos[1] - 20 / 2), size=(20, 20))
        for node in self.nodes:
            if node.collide_point(*pos):
                print('node collision!')
                node.try_connect_nodes(handle, (pos[0] - node.x, pos[1] - node.y))
        if self.line is not None:
            self.canvas.remove(self.line)
            self.line = None

    def on_connection_established(self, _, handles):
        connection = NodeConnectionData(*handles)
        self.connections.add(connection)
        connection.source_node.bind(pos=lambda *args: self.refresh_connection(connection))
        connection.sink_node.bind(pos=lambda *args: self.refresh_connection(connection))
        self.draw_connection(connection)

    def draw_connection(self, connection: NodeConnectionData):
        source_center = [connection.source_handle_offset[0] + connection.source_node.x + connection.source_handle.center_x,
                         connection.source_handle_offset[1] + connection.source_node.y + connection.source_handle.center_y]
        sink_center = [connection.sink_handle_offset[0] + connection.sink_node.x + connection.sink_handle.center_x,
                       connection.sink_handle_offset[1] + connection.sink_node.y + connection.sink_handle.center_y]
        points = [*source_center,
                  source_center[0] + ((sink_center[0] - source_center[0]) / 3), source_center[1],
                  source_center[0] + (2 * (sink_center[0] - source_center[0]) / 3), sink_center[1],
                  *sink_center]
        if connection.line is None:
            with self.canvas:
                Color(0, 0.8, 0.4)
                connection.line = Bezier(points=points, segments=50, dash_length=20, dash_offset=0)
        else:
            connection.line.points = points

    def refresh_connection(self, connection: NodeConnectionData):
        connection.recalculate_offsets()
        self.draw_connection(connection)
