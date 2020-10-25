# java type placeholders
from expr import Expr
from stmt import Stmt


class Void:
    pass


class Object:
    pass


class Null(Void, Expr, Stmt):
    def accept(self, visitor):
        return None

    def __bool__(self):
        return False
