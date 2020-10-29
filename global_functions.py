import time

from loxcallable import LoxCallable


class Clock(LoxCallable):
    def call(self):
        return time.time()

    def arity(self):
        return 0

    def __str__(self):
        return "<native_fn:Clock>"
