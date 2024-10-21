#!/usr/bin/env python3
from pymongo import MongoClient
''' Task 8's module '''


def listAll(mongo_collection):
    '''List all documents in a collection'''
    return [doc for doc in mongo_collection.find({})]
