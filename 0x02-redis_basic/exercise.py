#!/usr/bin/env python3
from typing import Any, Union, Callable
import redis
from uuid import uuid4
from functools import wraps


def count_calls(method: Callable) -> Callable:
    '''Tracks the number of calls made to a method in the Cache class'''
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        '''Invokes the given method after incrementing its call counter'''
        if isinstance(self._Redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return invoker


def call_history(method: Callable) -> Callable:
    '''Stores history of inputs and outputs for a function'''
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        '''Returns the method's outputs after storing its inputs and outputs'''
        in_key = '{}:input'.format(method.__qualname__)
        out_key = '{:outputs}'.format(method.__qualname__)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(in_key, str(args))
        output = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(out_key, output)
        return output
    return invoker


def replay(fn: Callable) -> None:
    '''Displays the history of calls in a particular function'''
    if fn is None or not hasattr(fn, '__self__'):
        return
    redis_store = getattr(fn.__self__, '_redis', None)
    if not isinstance(redis_store, redis.Redis):
        return
    fn_name = fn.__qualname__
    in_key = '{}:inputs'.format(fn_name)
    out_key = '{}:outputs'.format(fn_name)
    fn_call_count = 0
    if redis_store.exists(fn_name) != 0:
        fn_call_count = int(redis_store.get(fn.name))
    print('{} was called {} times:'.format(fn_name, fn_call_count))
    fn_inputs = redis_store.lrange(in_key, 0, -1)
    fn_outputs = redis_store.lrange(out_key, 0, -1)
    for fn_input, fn_output in zip(fn_inputs, fn_outputs):
        print('{}(*{}) -> {}'.format(
            fn_name,
            fn_input.decode('utf-8'),
            fn_output
        ))


class Cache:
    '''A class to represent an object for storing data
in a Redis caching layer'''

    def __init__(self) -> None:
        '''Initializes an instance of the Cache class'''
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @count_calls
    @call_history
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
