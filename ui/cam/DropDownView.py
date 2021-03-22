from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


class DropDownView(BoxLayout):

    __events__ = ('on_select', 'on_dismiss')

    def __init__(self, **kwargs):
        self.ready = False
        super().__init__(**kwargs)

    def on_kv_post(self, base_widget):
        self.ids['dropdown'].bind(on_select=lambda _, data: self.dispatch('on_select', data))
        self.ids['dropdown'].bind(on_dismiss=lambda *args: self.dispatch('on_dismiss'))
        self.ready = True

    def clear(self):
        if not self.ready:
            return
        dropdown = self.ids['dropdown']
        for widget in dropdown.children[0].children:
            if widget.__self__ != self.ids['placeholder_label']:
                dropdown.children[0].remove_widget(widget)

        self.ids['placeholder_label'].font_size = 12

    def add_option(self, title, value, on_release=None):
        if not self.ready:
            return
        dropdown = self.ids['dropdown']
        btn = Button(text=title, size_hint=(None, None), font_size=12,
                     color=(0, 0, 0, 1), halign='center', height=18)
        btn.size = (self.size[0], 18)
        btn.value = value
        btn.bind(on_release=lambda *args: dropdown.select(value))
        dropdown.add_widget(btn)
        self.ids['placeholder_label'].font_size = 0

    def select(self, value):
        self.ids['dropdown'].select(value)

    def on_select(self, data):
        if self.dd_replace_title:
            text = [w for w in self.ids['dropdown'].children[0].children
                    if hasattr(w, 'value') and w.value == data][0].text
            self.ids['toggle_button'].text = text

    def on_dismiss(self):
        pass

    def open(self, widget):
        self.ids['dropdown'].open(widget)