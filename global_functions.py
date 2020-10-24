import time

from loxcallable import LoxCallable


class Clock(LoxCallable):
    def call():
        return time.time()

    def arity():
        return 0

    def __str__():
        return "<native_fn:Clock>"
