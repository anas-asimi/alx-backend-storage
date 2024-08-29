#!/usr/bin/env python3
"""
exercise.py
"""
from typing import Union, Callable, Any
from functools import wraps
import uuid
import redis


def call_history(method: Callable) -> Callable:
    '''
    store the history of inputs and outputs for a particular function.
    '''
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        '''
        returns the given method after store the inputs and outputs.
        '''
        if isinstance(self._redis, redis.Redis):
            input_list_key = method.__qualname__ + ':inputs'
            self._redis.rpush(input_list_key, str(args))

        val = method(self, *args, **kwargs)

        if isinstance(self._redis, redis.Redis):
            output_list_key = method.__qualname__ + ':outputs'
            self._redis.rpush(output_list_key, val)

        return val
    return wrapper


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

    def __init__(self) -> None:
        """
        __init__
        """
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
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

    def get(self, key: str, fn=None) -> Union[str, bytes, int, float]:
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

    def get_str(self, key: str) -> str:
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

    def get_int(self, key: str) -> int:
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


def replay(method: Callable) -> None:
    """
    _summary_
    Args:
        method (_type_): _description_
    """
    # ["zip(", ".lrange("]
    self = method.__self__
    method_name = method.__qualname__
    count = self.get_int(method_name)
    input_list_key = method_name + ':inputs'
    input_list = self._redis.lrange(input_list_key, 0, -1)
    output_list_key = method_name + ':outputs'
    output_list = self._redis.lrange(output_list_key, 0, -1)
    print(f'{method_name} was called {count} times:')
    for i in range(0, len(input_list)):
        inputs = str(input_list[i], 'utf-8')
        outputs = str(output_list[i], 'utf-8')
        print(
            f"{method_name}(*{inputs}) -> {outputs}")
