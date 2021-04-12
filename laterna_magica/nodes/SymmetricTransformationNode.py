from .Node import Node
from .Meta import MetaBuilder, DataType
from typing import Any


class SymmetricTransformationNode(Node):
    def __init__(self):
        meta = MetaBuilder()\
            .with_input(DataType.RGBA)\
            .with_output(DataType.RGBA)\
            .build()
        super().__init__(meta)
        for i, inp in enumerate(self.inputs):
            assert inp.data_type == self.outputs[i].data_type, 'Invalid configuration: inputs and outputs must match' \
                                                               ' in count and data types!'
        self.preview = self.outputs[0]
        self.transform_fn = lambda inputs: [inp.value for inp in inputs]

    def on_input_changed(self, input_id: int, data: Any):
        results = self.transform_fn(self.inputs)
        for i, val in enumerate(results):
            self.outputs[i] = val
