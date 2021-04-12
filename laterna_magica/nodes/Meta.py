import enum
from typing import List, Tuple, Union, Dict, Callable, Any

import numpy as np


class Meta:

    def __init__(self, config: 'MetaBuilder'):
        if not config.ready:
            raise ValueError('Invalid constructor call: Meta Builder not ready!')
        self.inputs: List[InputMeta] = config.inputs
        self.outputs: List[DataType] = config.outputs

    @classmethod
    def empty(cls):
        return MetaBuilder().build()


class DataType(enum.Enum):
    FLOAT = enum.auto()
    STRING = enum.auto()
    RGBA = enum.auto()
    NONE = enum.auto()


class DataBuilder:

    def __init__(self, data_type, target):
        self.data_type = data_type
        self.target = target

    def build(self) -> 'InputMeta':
        raise NotImplementedError


class InputMeta:

    def __init__(self, data_type: DataType):
        self._data_type: DataType = data_type

    @property
    def data_type(self) -> DataType:
        return self._data_type


class NumericInput(InputMeta):

    def __init__(self):
        super().__init__(DataType.FLOAT)


class StringInput(InputMeta):

    def __init__(self):
        super().__init__(DataType.STRING)


class ChoiceInput(InputMeta):

    def __init__(self, options: List[Tuple[str]], data_type: DataType):
        super().__init__(data_type)
        self.options = options


class ImageInput(InputMeta):

    def __init__(self):
        super().__init__(DataType.RGBA)


class ChoiceDataBuilder(DataBuilder):

    def __init__(self):
        self.options = []
        self.data_type = DataType.NONE
        super().__init__(ChoiceInput, 'inputs')

    def build(self):
        return ChoiceInput(self.options, self.data_type)

    def with_option(self, title, key, value) -> 'ChoiceDataBuilder':
        self.options.append((title, key, value))
        return self


class MetaBuilder:
    def __init__(self):
        self.inputs: List[InputMeta] = []
        self.outputs: List[DataType] = []
        self.active_item: Union[DataBuilder, None] = None

    def _with_any(self, data_type: Union[type, DataType], list_var: str):
        if self.active_item is not None:
            self.inputs.append(self.active_item.build())
            self.active_item = None

        # meta_list: List[InputMeta] = self.__getattribute__(list_var)

        if type(data_type) is not DataType:
            if type(data_type) is ChoiceInput:
                self.active_item = ChoiceDataBuilder()
            basic_data_type = input_to_data_type[data_type]
        else:
            basic_data_type = data_type

        if list_var == 'inputs':
            self.inputs.append(data_to_input_type[basic_data_type]())
        elif list_var == 'outputs':
            self.outputs.append(basic_data_type)
        else:
            raise ValueError(f'Invalid target list: {list_var}!')

    def with_input(self, input_type: DataType) -> 'MetaBuilder':
        self._with_any(input_type, 'inputs')
        return self

    def with_output(self, output_type: DataType) -> 'MetaBuilder':
        self._with_any(output_type, 'outputs')
        return self

    def apply(self, fns: Tuple[Callable[[DataBuilder], DataBuilder]]):
        assert self.active_item is not None, 'No element available to apply to!'
        for fn in fns:
            fn(self.active_item)

    def build(self) -> Meta:
        return Meta(self)

    @property
    def ready(self):
        return self.active_item is None


data_to_input_type: Dict[DataType, type] = {
    DataType.FLOAT: NumericInput,
    DataType.STRING: StringInput,
}

input_to_data_type: Dict[type, DataType] = {}

for key, val in data_to_input_type.items():
    input_to_data_type[val] = key


default_values: Dict[DataType, Any] = {
    DataType.FLOAT: 0.,
    DataType.STRING: '',
    DataType.NONE: None,
    DataType.RGBA: np.zeros(()),
}