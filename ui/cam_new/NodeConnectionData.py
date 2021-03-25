from ui.nodes.NodeConnectionHandle import NodeConnectionHandle


class NodeConnectionData:
    def __init__(self, source_handle: NodeConnectionHandle, sink_handle: NodeConnectionHandle):
        self.source_handle = source_handle
        self.sink_handle = sink_handle
        self.source_node = self.sink_node = self.source_handle_offset = self.sink_handle_offset = None
        self.line = None
        self.recalculate_offsets()

    def recalculate_offsets(self):
        self.source_node, self.source_handle_offset = self.source_handle.find_node_view_offset()
        self.sink_node, self.sink_handle_offset = self.sink_handle.find_node_view_offset()

    def __eq__(self, other):
        if isinstance(other, NodeConnectionData):
            return other.source_handle == self.source_handle and other.sink_handle == self.sink_handle
        return False

    def __hash__(self):
        return self.source_handle.__hash__() ^ self.sink_handle.__hash__()
