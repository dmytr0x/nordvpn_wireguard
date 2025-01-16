from collections.abc import Sequence

from src.btypes import Item


def select_single_item[T](items: Sequence[Item[T]]) -> T | None:
    for i, item in enumerate(items, 1):
        print(f"{i}. {item['title']}")

    num = input("Select item: ")
    try:
        num = int(num)
    except (ValueError, TypeError):
        return None

    return items[num - 1]["data"]


def int_or_none(value: str) -> int | None:
    try:
        n = int(value.strip())
    except (ValueError, TypeError):
        return None
    return n


def select_multiple_items[T](items: Sequence[Item[T]]) -> list[T] | None:
    for i, item in enumerate(items, 1):
        print(f"{i}. {item['title']}")

    raw_input = input(
        "Select items ( Examples: `42` or `1,2,3` or `10..25` ): "
    )

    if ".." in raw_input:
        f, t = raw_input.strip().split("..")
        _from, _to = int_or_none(f), int_or_none(t)
        if _from is None or _to is None:
            return None
        if 1 <= _from <= len(items) and 1 <= _to <= len(items) and _from < _to:
            return [items[n - 1]["data"] for n in range(_from, _to + 1)]

    elif "," in raw_input:
        _items = [
            items[n - 1]["data"]
            for rn in raw_input.strip().split(",")
            if (n := int_or_none(rn))
        ]
        return _items or None

    elif raw_input.strip().isnumeric():
        if n := int_or_none(raw_input):
            item = items[n - 1]["data"]
            return [item]

    return None
