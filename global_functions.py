import time

import ipdb  # type: ignore

from loxcallable import LoxCallable


class Clock(LoxCallable):
    def call(self, interpreter, arguments):
        return time.time()

    def arity(self):
        return 0

    def __str__(self):
        return "<native_fn:Clock>"


class Debug(LoxCallable):
    def call(self, interpreter, arguments):
        return ipdb.set_trace()

    def arity(self):
        return 0

    def __str__(self):
        return "<native_fn:Debug>"
