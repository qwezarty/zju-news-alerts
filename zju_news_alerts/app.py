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
from zju_news_alerts.request import Request
from zju_news_alerts.mail import Mail

class App:
    """main application"""

    def __init__(self, import_name):
        self.import_name = import_name
        self.sources = [Request("physics")]

    def source(self, name):
        self.source = Request(name)
        return self.source

    def serve(self):
        print("starting all worker")
        for source in self.sources:
            source.get()
            print("worker list complete, next will be 60s")
        time.sleep(60)

    def send(self):
        news = self.source.get()
        Mail(news).send()
