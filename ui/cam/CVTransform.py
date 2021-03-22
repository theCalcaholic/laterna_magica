from kivy.uix.boxlayout import BoxLayout
from .TransformObserver import TransformObserver


class CVTransformContainer(BoxLayout, TransformObserver):

    selected_transform = StringProperty()
