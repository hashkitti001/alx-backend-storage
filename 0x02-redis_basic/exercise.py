#!/usr/bin/env python3
from typing import List, Union
import redis
from uuid import uuid4


class Cache:
    '''A class to represent an object for storing data in a Redis caching layer'''

    def __init__(self) -> None:
        '''Initializes an instance of the Cache class'''
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''A method that takes a data argument and returns a string'''
        key = str(uuid4())
        self._redis.set(key,data)
        return data