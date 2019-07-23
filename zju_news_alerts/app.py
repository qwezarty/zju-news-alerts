# -*- coding: utf-8 -*-

"""
    zju_news_alerts.app
    ~~~~~~~~~~~~~~~~~~~~~
    The main application.
    :author: qwezarty
    :date: 02:40 pm Jul 17 2019
    :email: qwezarty@gmail.com
"""

import time
from pymongo import MongoClient
from zju_news_alerts.request import Request
from zju_news_alerts.engine import Engine
from zju_news_alerts.mail import Mail

class App:
    """main application"""

    def __init__(self, import_name):
        self.import_name = import_name
        self.engine = Engine()
        self.sources = [
            Request("physics"),
            Request("grs")
        ]

    def source(self, name):
        self.source = Request(name)
        return self.source

    def serve(self):
        for source in self.sources:
            raw_news = source.list()
            cooked_news = self.engine.save_news(raw_news)
            for new in cooked_news:
                cooked_new = self.engine.with_more_infos(new)
                Mail(cooked_new).send()
        print("worker list complete, next will be 60s")
        time.sleep(60)

    def send(self):
        news = self.source.get()
        Mail(news).send()
