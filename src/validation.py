def int_or_none(value: str) -> int | None:
    """
    Attempts to convert a string to an integer.

    If the string cannot be converted (e.g., it contains invalid characters or is None),
    it returns None. Leading and trailing whitespace is stripped before conversion.

    Args:
        value (str): The string to be converted to an integer.

    Returns:
        int | None: The integer value if the conversion succeeds, otherwise None.

    Examples:
        >>> int_or_none("42")
        42
        >>> int_or_none("  15  ")
        15
        >>> int_or_none("not a number")
        None
        >>> int_or_none(None)
        None
    """

    try:
        n = int(value.strip())
    except (ValueError, TypeError):
        return None
    return n


def int_in_range(value: int, low: int, high: int) -> int | None:
    """
    Checks if an integer is within a specified range (inclusive).

    If the integer is within the range, it is returned as-is. Otherwise, it returns None.

    Args:
        value (int): The integer to be checked.
        low (int): The lower bound of the range (inclusive).
        high (int): The range's upper bound (inclusive).

    Returns:
        int | None: The input integer if it falls within the range, otherwise None.

    Examples:
        >>> int_in_range(42, 10, 50)
        42
        >>> int_in_range(5, 10, 50)
        None
        >>> int_in_range(60, 10, 50)
        None
    """

    if low <= value <= high:
        return value
    return None


def int_from_str(value: str, *, low: int, high: int) -> int | None:
    """
    Converts a string to an integer and checks if it falls within a specified range.

    First attempts to convert the string to an integer using `int_or_none`. If the conversion
    succeeds, it verifies that the integer is within the range `[low, high]` using
    `int_in_range`. Returns None if either step fails.

    Args:
        value (str): The string to be converted to an integer.
        low (int): The lower bound of the range (inclusive).
        high (int): The range's upper bound (inclusive).

    Returns:
        int | None: The integer value if conversion and range validation succeed, otherwise None.

    Examples:
        >>> int_from_str("42", low=10, high=50)
        42
        >>> int_from_str("5", low=10, high=50)
        None
        >>> int_from_str("not a number", low=10, high=50)
        None
    """

    if num := int_or_none(value):
        return int_in_range(num, low, high)
    return None
