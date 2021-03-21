from kivy.uix.button import Button
from kivy.properties import StringProperty
from kivy.uix.dropdown import DropDown
from kivy.graphics.texture import Texture, TextureRegion
from kivy.uix.boxlayout import BoxLayout
from .ObservableTransform import ObservableTransform
from .TransformObserver import TransformObserver
from .ObservableCameraTransform import ObservableCamera
from typing import Union, Callable, Dict


class SimpleTransform(BoxLayout, TransformObserver):

    selected_transform = StringProperty()

    def __init__(self, source: Union[ObservableTransform, ObservableCamera], **kwargs):
        self.transform_fns: Dict[
            str, Callable[[Union[Texture, TextureRegion]], Union[Texture, TextureRegion]]] = {
            'none': ObservableTransform.generic_transform,
            'mirror': SimpleTransform.mirror_transform,
            'flip': SimpleTransform.flip_transform
        }

        self.transform = ObservableTransform()
        self.bind(selected_transform=self.update_transform)
        self.selected_transform = 'none'

        super().__init__(**kwargs)
        self.set_source(source)

    def on_kv_post(self, base_widget):
        dropdown = self.ids['transform_selection']
        dropdown_toggle = self.ids['transform_selection_toggle']
        for tf_key in self.transform_fns.keys():
            def fn(b: Button):
                dropdown.select(b.text)
                dropdown_toggle.text = 'Select an Effect' if b.text == 'none' else b.text

            btn = Button(text=tf_key, size_hint=(None, None), font_size=12,
                         on_release=fn,
                         halign='center', height=18)
            dropdown.add_widget(btn)
            #btn.size = (dropdown.size[0], btn.texture_size[1])
        dropdown.bind(on_select=lambda _, choice: setattr(self, 'selected_transform', choice))
        self.transform.preview = self.ids['preview']

    def update_transform(self, *args):
        print(f"{self.selected_transform} is selected")
        self.transform.transform_fn = self.transform_fns[self.selected_transform]

    def notify_new_frame(self, texture):
        super(SimpleTransform, self).notify_new_frame(texture)
        self.transform.on_new_frame(texture)

    @classmethod
    def mirror_transform(cls, texture: Union[Texture, TextureRegion]):
        texture.flip_horizontal()
        return texture

    @classmethod
    def flip_transform(cls, texture: Union[Texture, TextureRegion]):
        texture.flip_vertical()
        return texture
