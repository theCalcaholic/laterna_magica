from kivy.properties import ListProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from typing import Callable


class AddTransformDialog(BoxLayout):

    transform_options = ListProperty()
    visible = BooleanProperty()

    __events__ = ('on_add_transform',)

    def __init__(self, **kwargs):
        self.is_name_valid: Callable = lambda _: True
        self._orig_parent = self.parent
        super().__init__(**kwargs)

    def on_kv_post(self, base_widget):
        self.bind(transform_options=self.rebuild_dropdown_menu)
        self._orig_parent = self.parent
        self.bind(visible=self.apply_visibility)
        self.apply_visibility()

    def rebuild_dropdown_menu(self, *_):
        dropdown = self.ids['transform_type_dropdown']
        dropdown.clear()
        for key in self.transform_options:
            dropdown.add_option(key, key)

        # dropdown.bind(on_select=lambda _, choice: setattr(self, '_selected_type', choice))
        if dropdown.selection is None and len(self.transform_options) > 0:
            dropdown.select(self.transform_options[0])

    def confirm_dialog(self):
        name = self.ids['name_input'].text
        if not self.is_name_valid(name):
            print('Invalid name!')
            return
        transform_type = self.ids['transform_type_dropdown'].selection
        if transform_type is None:
            print('No node type selected!')
            return
        self.hide()
        self.dispatch('on_add_transform', transform_type, name)

    def validate_name(self, _, name):
        if not self.is_name_valid(name):
            print('Invalid name!')

    def on_add_transform(self, *args):
        pass

    def show(self):
        if self.parent is not None:
            return
        self._orig_parent.add_widget(self)
        self.visible = True

    def hide(self):
        if self.parent is None:
            return
        print('hiding!')
        if not hasattr(self.parent, '__hideable_components'):
            self.parent.__hideable_components = set()
        self.parent.__hideable_components.add(self)
        self._orig_parent = self.parent
        self.parent.remove_widget(self)
        self.visible = False

    def apply_visibility(self, *args):
        if self.visible:
            self.show()
        else:
            self.hide()

    # def get_root_parent(self):
    #     if self.bounding_box_widget is not None:
    #         return self.bounding_box_widget
    #     return self.parent
