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
