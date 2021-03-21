from .ObservableTransform import ObservableTransform
from .TransformObserver import TransformObserver


class ObservableTransformObserver(TransformObserver, ObservableTransform):

    def __init__(self):
        super().__init__()
        self.connect(self)
