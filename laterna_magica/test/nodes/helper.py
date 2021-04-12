from typing import Dict, Any
from laterna_magica.nodes import Observer, ObservableOutput, Node, Meta, MetaBuilder, DataType


class TestObserver(Observer):

    def __init__(self):
        self.results = []

    def notify(self, cause: ObservableOutput, data: Dict[str, Any]):
        self.results.append((cause, data))


class PassthroughNode(Node):
    def __init__(self):
        meta = MetaBuilder()\
            .with_input(DataType.FLOAT)\
            .with_output(DataType.FLOAT)\
            .build()
        self.results = []
        super().__init__(meta)

    def on_input_changed(self, input_id: int, data: Any):
        self.results.append((input_id, data))
        self.outputs[0].value = self.inputs[0].value
