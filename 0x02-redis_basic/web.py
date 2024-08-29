#!/usr/bin/env python3
'''
A module with tools for request caching and tracking.
'''
import redis
import requests
from functools import wraps
from typing import Callable


# The module-level Redis instance.
redis_store = redis.Redis()
redis_store.flushdb(True)


def data_cacher(method: Callable) -> Callable:
    '''
    Caches the output of fetched data.
    '''
    @wraps(method)
    def invoker(url) -> str:
        '''
        The wrapper function for caching the output.
        '''
        result = redis_store.get(f'result:{url}')
        if result:
            print(f'get {url} from cache')
            return result.decode('utf-8')
        return method(url)
    return invoker


@data_cacher
def get_page(url: str) -> str:
    '''
    Returns the content of a URL after caching the request's response,
    and tracking the request.
    '''
    print(f'get {url} from internet')
    result = requests.get(url).text
    redis_store.incr(f'count:{url}')
    redis_store.setex(f'result:{url}', 10, result)
    return result


if __name__ == "__main__":
    time = __import__('time')
    get_page('https://www.google.com/')
    get_page('https://www.google.com/')
    time.sleep(8)
    get_page('https://www.google.com/')
    time.sleep(2)
    get_page('https://www.google.com/')
