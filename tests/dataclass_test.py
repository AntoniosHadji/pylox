from dataclasses import dataclass


class N:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c


n = N(1, 2, 3)
print(n)
d = {n: "normal_class"}
print(d)


@dataclass(frozen=True)
class D:
    a: int
    b: int
    c: int


d1 = D(1, 2, 3)
print(d1)
print(type(d1))
print(type(n))
d2 = D(1, 2, 3)
print(d2)
print("id(d2):", id(d2))
print("id(d1):", id(d1))
print(d1 == d2)
print(d1 == n)
print(hash(n))
print(hash(d1))
print(hash(d2))


@dataclass(frozen=True, eq=False)
class E:
    a: int
    b: int
    c: int


e = E(1, 2, 3)
f = E(1, 2, 3)
print(e, f)
print(e == f)
print(hash(e), hash(f))
d.update({d1: "dataclass1", d2: "dataclass2"})
print(d)
d.update({e: "dataclass1", f: "dataclass2"})
print(d)
