from collections.abc import Sequence
from functools import partial

from src import validation
from src.btypes import Item


def select_single_item[T](items: Sequence[Item[T]]) -> T | None:
    for i, item in enumerate(items, 1):
        print(f"{i}. {item['title']}")  # noqa: T201

    raw_input = input("Select item: ")
    if num := validation.int_from_str(raw_input, low=1, high=len(items)):
        return items[num - 1]["data"]

    return None


def select_multiple_items[T](items: Sequence[Item[T]]) -> list[T] | None:
    int_from_str = partial(validation.int_from_str, low=1, high=len(items))

    for i, item in enumerate(items, 1):
        print(f"{i}. {item['title']}")  # noqa: T201

    raw_input = input("Select items ( Examples: `42` or `1,2,3` or `10..25` ): ")

    if ".." in raw_input:
        f, t = raw_input.strip().split("..")

        _from, _to = int_from_str(f), int_from_str(t)
        if _from is None or _to is None:
            return None
        if _from < _to:
            return [items[n - 1]["data"] for n in range(_from, _to + 1)]

    elif "," in raw_input:
        items_data = [
            items[n - 1]["data"]
            for raw_number in raw_input.strip().split(",")
            if (n := int_from_str(raw_number))
        ]
        return items_data or None

    elif raw_input.strip().isnumeric():
        if n := int_from_str(raw_input):
            item_data = items[n - 1]["data"]
            return [item_data]

    return None
