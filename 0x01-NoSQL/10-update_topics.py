#!/usr/bin/env python3
from pymongo import MongoClient
''' Task 10's module '''


def update_topics(mongo_collection, name, topics):
    '''A Python function that updates the topics attr of a document in a collection with a given name '''
    mongo_collection.update_many(
        {'name': name},
        {'$set': {'topics': topics}}
    )

