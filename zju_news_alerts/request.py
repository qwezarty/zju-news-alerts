# -*- coding: utf-8 -*-

"""
    zju_news_alerts.request
    ~~~~~~~~~~~~~~~~~~~~~
    Base request class of diffrent source.
    :author: qwezarty
    :date: 03:14 pm Jul 17 2019
    :email: qwezarty@gmail.com
"""

import requests
from zju_news_alerts.wrapper import mail_errors
from zju_news_alerts.sources.physics import Physics
from zju_news_alerts.sources.grs import GRS
import zju_news_alerts.helpers as helpers
from lxml import etree

class Request:
    def __init__(self, source_name):
        self.source_name = ''
        self.source = self._get_source(source_name)
        self._source_func(self.source)
        self.headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.2 Safari/605.1.15'}
        self.session = requests.Session()

    def _get_source(self, source_name):
        if source_name == 'physics':
            self.source_name = 'physics'
            return Physics(base_url='http://physics.zju.edu.cn/chinese/redir.php?catalog_id=12267')
        elif source_name == 'grs':
            self.source_name = 'grs'
            return GRS()
        else:
            raise Exception("no source matched: %s" % source_name)

    def _source_func(self, source):
        if (not hasattr(source, 'analyze_list') or
                not hasattr(source, 'analyze_detail')):
            raise Exception("analyze_list() and analyze_detail() is required for every source!")
        if not hasattr(source, 'get_list_url'):
            def get_list_url():
                return source.base_url
            source.get_list_url = get_list_url
        if not hasattr(source, 'get_list_qs'):
            def get_list_qs():
                return {}
            source.get_list_qs = get_list_qs
        if not hasattr(source, 'get_info_qs'):
            def get_info_qs():
                return {}
            source.get_info_qs = get_info_qs

    @mail_errors
    def list(self):
        url = self.source.get_list_url()
        params = self.source.get_list_qs()
        res = self.session.get(url=url, headers=self.headers, params=params, timeout=30)
        if not res:
            raise Exception("request list gives none response, source: %s" % self.source_name)
        res.encoding = self.source.encoding
        helpers.cache_response(response=res, encoding=self.source.encoding)
        text = res.text.encode(res.encoding).decode(self.source.encoding)
        html = etree.HTML(text)
        rets = self.source.analyze_list(html)
        rets.sort(key=lambda x: x["date"], reverse=True)
        return rets

    @mail_errors
    def get(self):
        latest = self.list()[0]
        params = self.source.get_info_qs()
        try:
            res = self.session.get(url=latest["url"], headers=self.headers, params=params, timeout=30)
        except requests.exceptions.ConnectTimeout as error:
            raise error
        if not res:
            raise Exception("request detail gives none response, source: %s" % self.source_name)
        res.encoding = self.source.encoding
        helpers.cache_response(response=res, encoding=self.source.encoding)
        text = res.text.encode(res.encoding).decode(self.source.encoding)
        html = etree.HTML(text)
        return self.source.analyze_detail(html)

