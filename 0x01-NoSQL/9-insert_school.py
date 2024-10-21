#!/usr/bin/env python3
from pymongo import MongoClient
''' Task 9's module '''


def insert_school(mongo_collection, **kwargs):
    '''A Python function that inserts a new document in a collection based on kwargs'''
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id

