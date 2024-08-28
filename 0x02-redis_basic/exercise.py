#!/usr/bin/env python3
"""
exercise.py
"""
from typing import Union, Callable, Any
from functools import wraps
import uuid
import redis


def count_calls(method: Callable) -> Callable:
    '''
    Tracks the number of calls made to a method in a Cache class.
    '''
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        '''
        returns the given method after incrementing its call counter.
        '''
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


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

    @count_calls
    def store(self, data: Union[str, int, float, bytes]):
        """
        store
        Args:
            data (Union[str, int, float, bytes]): _description_
        """
        if type(data) not in [str, int, float, bytes]:
            return None
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn=None):
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
