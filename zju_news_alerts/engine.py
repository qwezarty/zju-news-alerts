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
        self.news = db.news
        self.sources = db.sources
        # time filter
        self.start = datetime.now()
        # inserting sources to db
        self._init_sources()

    def save_news(self, news):
        news = self._filter_news(self, news)
        # todo error handling, query before return
        rets = self.news.insert_many(news)
        return news

    def with_more_infos(self, new):
        source = self.sources.find_one({"_id": new["source"]})
        if source:
            new["source"] = source
        return new

    def _filter_news(self, news):
        rets = []
        for new in news:
            if new["date"] < self.start:
                continue
            ret = self.news.find_one(new)
            if ret:
                continue
            rets.append(new)
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

