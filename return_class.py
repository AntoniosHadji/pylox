from java_types import Object


class Return(RuntimeError):
    def __init__(self, value: Object):
        super().__init__()
        self.value = value
