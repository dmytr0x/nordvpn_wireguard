from typing import TypedDict


class Item[T](TypedDict):
    title: str
    data: T


class NameValue(TypedDict):
    name: str
    value: str
