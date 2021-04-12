from .Node import Node
from .Meta import MetaBuilder, DataType
from typing import Any


class PreviewNode(Node):
    def __init__(self):
        meta = MetaBuilder()\
            .with_input(DataType.RGBA)\
            .with_output(DataType.RGBA)\
            .build()
        super().__init__(meta)
        self.preview = self.outputs[0]

    def on_input_changed(self, input_id: int, data: Any):
        self.outputs[0].value = self.inputs[0].value
