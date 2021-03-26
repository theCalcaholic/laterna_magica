from kivy.event import EventDispatcher
from kivy.uix.widget import Widget
from kivy.properties import StringProperty, AliasProperty
from transforms.LinkedTransform import LinkedTransform
import numpy as np
from typing import Union


def get_name(instance):
    return instance._name


def set_name(instance, value):
    if instance.name_is_valid(value):
        if instance._name in AbstractTransformNodeView.registered_names:
            AbstractTransformNodeView.registered_names.remove(instance._name)
        AbstractTransformNodeView.registered_names.add(value)
        instance._name = value
        return True


class AbstractTransformNodeView(Widget):

    name = AliasProperty(get_name, set_name)
    registered_names = set()

    def __init__(self, prefix, **kwargs):
        self._name = None
        self.name = AbstractTransformNodeView.find_available_name(prefix)
        assert self.name is not None
        self.transform: Union[LinkedTransform, None] = None
        self.transform_init(self.name)
        super().__init__(**kwargs)

    @classmethod
    def find_available_name(cls, prefix=''):
        num = 1
        name = f'{prefix}'
        while name in cls.registered_names:
            name = f'{prefix} {num:03}'
            num += 1
        return name

    def transform_init(self, name):
        raise NotImplementedError()

    def on_kv_post(self, *args):
        assert self.name is not None
        self.transform.bind(on_frame_processed=self.frame_received)

    def frame_received(self, instance: LinkedTransform, source: LinkedTransform):
        pass

    def name_is_valid(self, name: str) -> bool:
        return name == self.name or name not in AbstractTransformNodeView.registered_names
