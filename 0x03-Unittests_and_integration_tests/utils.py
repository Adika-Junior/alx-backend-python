#!/usr/bin/env python3
"""Utility functions for nested map access, JSON fetching, and memoization."""
import requests
from functools import wraps
from typing import Any, Mapping, Sequence


def access_nested_map(nested_map: Mapping, path: Sequence) -> Any:
    """Access a nested map using a sequence of keys.

    Args:
        nested_map: A nested dictionary structure.
        path: A sequence of keys to access nested values.

    Returns:
        The value at the specified path in the nested map.

    Raises:
        KeyError: If any key in the path is missing.
    """
    for key in path:
        if not isinstance(nested_map, Mapping):
            raise KeyError(key)
        nested_map = nested_map[key]
    return nested_map


def get_json(url: str) -> dict:
    """Fetch JSON data from a URL.

    Args:
        url: The URL to fetch JSON from.

    Returns:
        A dictionary containing the JSON response.
    """
    response = requests.get(url)
    return response.json()


def memoize(func):
    """Decorator to memoize method calls and turn them into properties.

    Caches the result of a method call and converts the method into a property
    that returns the cached value on subsequent accesses.

    Args:
        func: The method to memoize.

    Returns:
        A property that caches the method's result.
    """
    attr_name = "_{}".format(func.__name__)

    @wraps(func)
    def memoized(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, func(self))
        return getattr(self, attr_name)

    return property(memoized)

