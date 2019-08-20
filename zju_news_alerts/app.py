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

    def warmup(self):
        for source in self.sources:
            posts = source.list()
            self.engine.save_posts(posts)
        print("warmup successfully, please serve now")

    def serve(self):
        while True:
            for source in self.sources:
                try:
                    raw_posts = source.list()
                    cooked_posts = self.engine.save_posts(raw_posts)
                except error:
                    # todo mail error to maintainer
                    print(error)
                    continue
                for post in cooked_posts:
                    try:
                        post = source.get(post["url"])
                        post = self.engine.with_more_infos(post)
                        Mail(post).send()
                    except:
                        # todo mail error to maintainer
                        print("sending mail failed, post: %s" % post["title"])
                        continue
            print("worker list complete, next will be 1hr")
            time.sleep(3600)

    def send(self):
        post = self.source.get()
        cooked_post = self.engine.with_more_infos(post)
        Mail(cooked_post).send()
