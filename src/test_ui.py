# ruff: noqa: ANN001, ANN101, ANN201, S101
from unittest.mock import patch

import pytest

from src import ui


@pytest.fixture
def sample_items():
    return [
        {"title": "Item 1", "data": 10},
        {"title": "Item 2", "data": 20},
        {"title": "Item 3", "data": 30},
    ]


def test_select_single_item_valid_input(sample_items):
    with patch("builtins.input", return_value="2"):
        assert ui.select_single_item(sample_items) == 20

    with patch("builtins.input", return_value="1"):
        assert ui.select_single_item(sample_items) == 10

    with patch("builtins.input", return_value="3"):
        assert ui.select_single_item(sample_items) == 30


def test_select_single_item_invalid_input(sample_items):
    with patch("builtins.input", return_value="0"):
        assert ui.select_single_item(sample_items) is None

    with patch("builtins.input", return_value="4"):
        assert ui.select_single_item(sample_items) is None

    with patch("builtins.input", return_value="not a number"):
        assert ui.select_single_item(sample_items) is None

    with patch("builtins.input", return_value=""):
        assert ui.select_single_item(sample_items) is None

    with patch("builtins.input", return_value="💩"):
        assert ui.select_single_item(sample_items) is None


def test_select_multiple_items_valid_inputs(sample_items):
    with patch("builtins.input", return_value="2"):
        assert ui.select_multiple_items(sample_items) == [20]

    with patch("builtins.input", return_value="1,3"):
        assert ui.select_multiple_items(sample_items) == [10, 30]

    with patch("builtins.input", return_value="1..3"):
        assert ui.select_multiple_items(sample_items) == [10, 20, 30]


def test_select_multiple_items_invalid_inputs(sample_items):
    with patch("builtins.input", return_value="0"):
        assert ui.select_multiple_items(sample_items) is None

    with patch("builtins.input", return_value="4"):
        assert ui.select_multiple_items(sample_items) is None

    with patch("builtins.input", return_value="not a number"):
        assert ui.select_multiple_items(sample_items) is None

    with patch("builtins.input", return_value="1,not_a_number"):
        assert ui.select_multiple_items(sample_items) == [10]

    with patch("builtins.input", return_value=""):
        assert ui.select_multiple_items(sample_items) is None

    with patch("builtins.input", return_value="3..1"):
        assert ui.select_multiple_items(sample_items) is None


def test_select_multiple_items_edge_cases(sample_items):
    with patch("builtins.input", return_value="1..1"):
        assert ui.select_multiple_items(sample_items) == [10]

    with patch("builtins.input", return_value="3..3"):
        assert ui.select_multiple_items(sample_items) == [30]

    with patch("builtins.input", return_value="1,1,3"):
        assert ui.select_multiple_items(sample_items) == [10, 10, 30]
