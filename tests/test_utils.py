import pytest

from kssspace.utils import exclude_keys


@pytest.mark.parametrize(
    "input_dict, keys_to_exclude, expected_output",
    [
        (
            {"name": "Eric Normand", "age": 35, "country": "USA"},
            ["age"],
            {"name": "Eric Normand", "country": "USA"},
        ),
        ({"a": 1, "b": 2, "c": 3, "d": 4}, ["b", "d"], {"a": 1, "c": 3}),
        (
            {"key1": "value1", "key2": "value2"},
            ["key3"],
            {"key1": "value1", "key2": "value2"},
        ),
        # Add more test cases here as needed
    ],
)
def test_exclude_keys(input_dict, keys_to_exclude, expected_output):
    result = exclude_keys(input_dict, keys_to_exclude)
    assert result == expected_output
