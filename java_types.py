# java type placeholders
from typing import Any


class Void:
    pass


class Object(Any):
    pass


class Null(Any):
    def accept(self, visitor):
        return None
