from dataclasses import dataclass


class N:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c


@dataclass(frozen=True)
class D:
    a: int
    b: int
    c: int


@dataclass(frozen=True, eq=False)
class E:
    a: int
    b: int
    c: int


def test_normal_class():
    # normal
    n1 = N(1, 2, 3)
    n2 = N(1, 2, 3)
    d = {n1: "normal_class 1", n2: "normal_class 2"}
    assert len(d) == 2


def test_frozen_dataclass():
    # frozen
    d1 = D(1, 2, 3)
    d2 = D(1, 2, 3)
    n = N(1, 2, 3)
    assert id(d1) != id(d2)
    assert d1 == d2
    assert d1 != n
    assert d2 != n
    assert hash(d1) == hash(d2)
    assert hash(d1) != hash(n)
    assert hash(d2) != hash(n)


def test_frozen_eq_dataclass():
    # frozen + eq
    e = E(1, 2, 3)
    f = E(1, 2, 3)
    assert e != f
    assert id(e) != id(f)
    assert hash(e) != hash(f)


def test_dict():
    d1 = D(1, 2, 3)
    d2 = D(1, 2, 3)
    e = E(1, 2, 3)
    f = E(1, 2, 3)
    n = N(1, 2, 3)
    d = {n: "normal_class"}
    assert len(d) == 1
    d.update({d1: "dataclass1", d2: "dataclass2"})
    assert len(d) == 2
    d.update({e: "dataclass1", f: "dataclass2"})
    assert len(d) == 4
