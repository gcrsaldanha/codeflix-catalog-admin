from dataclasses import dataclass


@dataclass
class User:
    id: int
    name: str
    age: int

    def __eq__(self, other):
        # class
        return self.id == other.id


@dataclass(frozen=True)
class MonetaryValue:
    value: float
    currency: str


a = MonetaryValue(10, "BRL")
b = MonetaryValue(10, "BRL")

assert a == MonetaryValue(10, "BRL")  # True
