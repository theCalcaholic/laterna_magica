import weakref
from typing import TYPE_CHECKING, List, Union, Dict, Any
from laterna_magica.nodes import Meta, Observer, ObservableOutput

if TYPE_CHECKING:
    import numpy as np


class Node(Observer):

    def __init__(self, meta: Meta):
        self.meta: Meta = Meta.empty() if meta is None else meta
        self.inputs: List[Union[ObservableOutput, weakref.ProxyType[ObservableOutput]]] = []
        self.outputs: List[ObservableOutput] = []
        self.preview: Union[ObservableOutput, None] = None

        self.inputs = []
        for inp in self.meta.inputs:
            self.inputs.append(ObservableOutput(inp.data_type))
            self.inputs[-1].register(self)
        self.outputs = [ObservableOutput(data_type, self) for data_type in self.meta.outputs]

    def attach_to(self, output: ObservableOutput, input_id: int):
        assert output.data_type == self.meta.inputs[input_id].data_type

        if self.inputs[input_id] is not None:
            self.inputs[input_id].unregister(self)
        self.inputs[input_id] = weakref.proxy(output)
        self.inputs[input_id].register(self)

    def notify(self, cause: 'ObservableOutput', data: Any):
        self.on_input_changed(self.inputs.index(cause), data)

    def on_input_changed(self, input_id: int, data: Any):
        pass
