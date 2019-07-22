# -*- coding: utf-8 -*-

"""
    zju_news_alerts.sources.physics
    ~~~~~~~~~~~~~~~~~~~~~
    Source of physics, i.e. http://physics.zju.edu.cn
    :author: qwezarty
    :date: 03:10 pm Jul 17 2019
    :email: qwezarty@gmail.com
"""

import uuid
import io
from zju_news_alerts import helpers
from lxml import etree
from dateutil.parser import parse

class Physics:
    def __init__(self, base_url=''):
        self.base_url = base_url or 'http://physics.zju.edu.cn/chinese/redir.php'
        self.encoding = 'gb2312'

    def analyze_list(self, html):
        items = html.xpath('//ul[@class="cg-news-list"]/li')
        rets = []
        for item in items:
            rets.append(self._analyze_list_item(item))
        return rets

    def _analyze_list_item(self, item):
        item = etree.HTML(etree.tostring(item))
        title = helpers.xpath_text(item, '//a', 'title')
        raw_date = helpers.xpath_text(item, '//span')
        cooked_date = parse(raw_date)
        url = 'http://physics.zju.edu.cn/chinese/' + helpers.xpath_text(item, '//a', 'href')
        return {'id': str(uuid.uuid1()), 'title': title, 'date': cooked_date, 'url': url}

    def analyze_detail(self, html):
        title = helpers.xpath_text(html, '//h2[@class="art-heading"]')
        content_element = html.xpath('//div[contains(@class, "art-content")]')
        assert len(content_element) == 1, 'news content should only have one'
        abs_path = helpers.cache_element(content_element[0], title)
        return {'title': title, 'path': abs_path}

