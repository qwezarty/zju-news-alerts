# -*- coding: utf-8 -*-

"""
    zju_news_alerts.engine
    ~~~~~~~~~~~~~~~~~~~~~
    Connections to mongodb.
    :author: qwezarty
    :date: 09:06 am Jul 23 2019
    :email: qwezarty@gmail.com
"""

from dateutil.parser import parse
from datetime import datetime
from pymongo import MongoClient

class Engine:
    def __init__(self, addr='localhost', port=27017):
        # setting up mongo collections
        db = MongoClient(addr, port)["zna"]
        self.posts = db.posts
        self.sources = db.sources
        # time filter
        self.start = parse("2018-01-01")
        # inserting sources to db
        self._init_sources()

    def save_posts(self, posts, filter=True):
        if filter:
            posts = self._filter_posts(posts)
        if len(posts) > 0:
            # todo error handling, query before return
            rets = self.posts.insert_many(posts)
        return posts

    def with_more_infos(self, post):
        if not post:
            return []
        source = self.sources.find_one({"_id": post["source"]})
        if source:
            post["source"] = source
        return post

    def _filter_posts(self, posts):
        rets = []
        if not posts:
            return rets
        for post in posts:
            if post["date"] < self.start:
                continue
            ret = self.posts.find_one(post)
            if ret:
                continue
            rets.append(post)
        return rets

    def _init_sources(self):
        sources = [
            {
                "_id": "physics",
                "description": "zju, department of physics",
                "subscribers": ["qwezarty@163.com"]
            },
            {
                "_id": "grs",
                "description": "zju, postgraduate research institute",
                "subscribers": ["qwezarty@163.com"]
            }
        ]
        for source in sources:
            if self.sources.find_one({"_id": source["_id"]}):
                self.sources.update_one({"_id": source["_id"]}, {"$set": source})
            else:
                self.sources.insert_one(source)

