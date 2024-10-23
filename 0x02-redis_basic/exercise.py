#!/usr/bin/env python3
from typing import List, Union, Callable
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
        self._redis.set(key, data)
        return data

    def get(
        self, key: str,
        fn: Callable = None
    ) -> Union[str, bytes, int, float]:
        '''Retrieves a value from a Redis caching layer'''
        gotten = self._redis.get(key)
        # Keeps original Redis.get behavior by returning 
        # affected data
        return fn(gotten) if fn is not None else gotten
    
    def get_str(self, key: Union[str, bytes, int, float]):
        '''Returns the string converted value from the Redis storage'''
        return self.get(key, lambda x: x.decode('utf-8'))
    
    def get_int(self, key: Union[str, bytes, int, float]):
        '''Returns the int representation of a value stored in Redis store'''
        return self.get(key, lambda x: int(x))
    
    