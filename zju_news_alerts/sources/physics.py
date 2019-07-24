# -*- coding: utf-8 -*-

"""
    zju_news_alerts.sources.physics
    ~~~~~~~~~~~~~~~~~~~~~
    Source of physics, i.e. http://physics.zju.edu.cn
    :author: qwezarty
    :date: 03:10 pm Jul 17 2019
    :email: qwezarty@gmail.com
"""

import io
from zju_news_alerts import helpers
from lxml import etree
from dateutil.parser import parse

class Physics:
    def __init__(self, source_name='', base_url=''):
        self.base_url = base_url or 'http://physics.zju.edu.cn/chinese/redir.php'
        self.source_name = source_name or 'physics'
        self.encoding = 'gb2312'

    def analyze_list(self, html):
        items = html.xpath('//ul[@class="cg-news-list"]/li')
        rets = []
        for item in items:
            rets.append(self._analyze_list_item(item))
        return rets

    def _analyze_list_item(self, item):
        item = etree.HTML(etree.tostring(item))
        title = helpers.xpath(item, '//a', 'title')
        raw_date = helpers.xpath(item, '//span')
        cooked_date = parse(raw_date)
        url = 'http://physics.zju.edu.cn/chinese/' + helpers.xpath(item, '//a', 'href')
        return {'source': self.source_name, 'title': title, 'date': cooked_date, 'url': url}

    def analyze_detail(self, html):
        title = helpers.xpath(html, '//h2[@class="art-heading"]')
        content_element = html.xpath('//div[contains(@class, "art-content")]')
        assert len(content_element) == 1, 'news content should only have one'
        abs_path = helpers.cache_element(content_element[0], title)
        return {'source': self.source_name, 'title': title, 'path': abs_path}

