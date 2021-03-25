from .LinkedTransform import LinkedTransform


class SourceTransform(LinkedTransform):

    def __init__(self, name, *args, **kwargs):
        super().__init__(name, *args, **kwargs)
        self.input_channels = []
