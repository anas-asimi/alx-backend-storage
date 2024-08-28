#!/usr/bin/env python3
"""
exercise.py
"""
from typing import Union
import uuid
import redis


class Cache:
    """
    Cache
    """

    def __init__(self):
        """
        __init__
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, int, float, bytes]):
        """
        store
        Args:
            data (Union[str, int, float, bytes]): _description_
        """
        if type(data) in [str, int, float, bytes]:
            key = str(uuid.uuid4())
            self._redis.set(key, data)
            return key
        return None

    def get(self, key: str, fn):
        """
        get
        Args:
            key (str): _description_
            fn (function): _description_
        Returns:
            _type_: _description_
        """
        binary_value = self._redis.get(key)
        if binary_value is None:
            return None
        if fn:
            return fn(binary_value)
        return binary_value

    def get_str(self, key: str):
        """
        get_str
        Args:
            key (str): _description_
        Returns:
            _type_: _description_
        """
        binary_value = self._redis.get(key)
        if binary_value is None:
            return None
        return str(binary_value)

    def get_int(self, key: str):
        """
        get_int
        Args:
            key (str): _description_
        Returns:
            _type_: _description_
        """
        binary_value = self._redis.get(key)
        if binary_value is None:
            return None
        return int(binary_value)
