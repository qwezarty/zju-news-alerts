# -*- coding: utf-8 -*-

"""
    zju_news_alerts.engine
    ~~~~~~~~~~~~~~~~~~~~~
    Connections to mongodb.
    :author: qwezarty
    :date: 09:06 am Jul 23 2019
    :email: qwezarty@gmail.com
"""

from datetime import datetime
from pymongo import MongoClient

class Engine:
    def __init__(self, addr='localhost', port=27017):
        # setting up mongo collections
        db = MongoClient(addr, port)["zna"]
        self.posts = db.posts
        self.sources = db.sources
        # time filter
        self.start = datetime.now()
        # inserting sources to db
        self._init_sources()

    def save_posts(self, posts):
        posts = self._filter_posts(self, posts)
        # todo error handling, query before return
        rets = self.posts.insert_many(posts)
        return posts

    def with_more_infos(self, post):
        source = self.sources.find_one({"_id": post["source"]})
        if source:
            post["source"] = source
        return post

    def _filter_posts(self, posts):
        rets = []
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
            {"_id": "physics", "description": "zju, department of physics", "subscribers": ["qwezarty@163.com"]},
            {"_id": "grs", "description": "zju, postgraduate research institute", "subscribers": ["qwezarty@163.com"]}
        ]
        for source in sources:
            if self.sources.find_one(source):
                continue
            self.sources.insert_one(source)

