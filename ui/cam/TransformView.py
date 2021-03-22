from .SimpleTransform import SimpleTransform
from kivy.uix.boxlayout import BoxLayout


class TransformView(BoxLayout):

    __events__ = ('on_ready',)

    def __init__(self, index, **kwargs):
        self.index = index
        self.transform_view = None
        self.transform_types = {'Simple': lambda: SimpleTransform()}
        super().__init__(**kwargs)

    def on_kv_post(self, base_widget):
        super(TransformView, self).on_kv_post(base_widget)
        self.fill_dropdown()

    def on_ready(self, *args):
        pass

    def activate(self, transform_registry):
        source = transform_registry.register(self.index, self.transform_view.transform)
        self.transform_view.set_source(source)

    def load_transform(self, transform_type):
        self.remove_widget(self.ids['transform_type_dropdown'])
        self.transform_view = transform_type()
        self.transform_view.size_hint = 1, 1
        self.add_widget(self.transform_view)
        self.dispatch('on_ready')

    def fill_dropdown(self):
        dropdown = self.ids['transform_type_dropdown']
        dropdown.clear()
        for title, transform_type in self.transform_types.items():
            print(transform_type)
            dropdown.add_option(title, title)
        dropdown.bind(on_select=lambda _, choice: self.load_transform(self.transform_types[title]))
