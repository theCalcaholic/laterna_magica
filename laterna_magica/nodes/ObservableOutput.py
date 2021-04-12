import weakref
from typing import TYPE_CHECKING, List, Set, Tuple, Any, Union
from laterna_magica.nodes.Meta import default_values

if TYPE_CHECKING:
    from laterna_magica.nodes import DataType, Observer, Node


class ObservableOutput:

    def __init__(self, data_type: 'DataType', provider=None):
        self.data_type = data_type
        self._value = default_values[data_type]
        self.observers: 'weakref.WeakSet[Observer]' = weakref.WeakSet()
        self.provider: Union[Node, None] = provider

    def register(self, observer: 'Observer'):
        self.observers.add(observer)

    def unregister(self, observer: 'Observer'):

        self.observers.remove(observer)

    def on_changed(self):
        for observer in self.observers:
            observer.notify(self, self.value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: float):
        self._value = value
        self.on_changed()
