# -*- coding: utf-8 -*-

"""
    zju_news_alerts.sources.physics
    ~~~~~~~~~~~~~~~~~~~~~
    Source of grs, i.e. http://grs.zju.edu.cn/
    :author: qwezarty
    :date: 09:16 am Jul 22 2019
    :email: qwezarty@gmail.com
"""

import io
from zju_news_alerts import helpers
from lxml import etree
from dateutil.parser import parse
from datetime import datetime

class GRS:
    def __init__(self, source_name='', base_url=''):
        self.base_url = base_url or 'http://grs.zju.edu.cn/'
        self.source_name = source_name or 'grs'
        self.encoding = 'utf-8'

    def analyze_list(self, html):
        items = html.xpath('//div[@class="contents"]//ul[@class="cg-news-list"]/li')
        helpers.cache_element(items[0])
        rets = []
        for item in items:
            rets.append(self._analyze_list_item(item))
        return rets

    def _analyze_list_item(self, item):
        item = etree.HTML(etree.tostring(item))
        title = helpers.xpath_text(item, '//li/a', 'title')
        type = helpers.xpath_text(item, '//li/span//a')
        raw_date = helpers.xpath_text(item, '//li/span[@class="art-date"]')
        cooked_date = parse(raw_date)
        url = 'http://grs.zju.edu.cn/' + helpers.xpath_text(item, '//li/a', 'href')
        return {'source': self.source_name, 'type': type, 'title': title, 'date': cooked_date, 'url': url}

    def analyze_detail(self, html):
        title = helpers.xpath_text(html, '//h2[@class="art-heading"]')
        raw_date = helpers.xpath_text(html, '//div[@class="art-summary"]/text()').replace(' ', '')
        cooked_date = datetime.strptime(raw_date, '%Y年%m月%d日%H:%M')
        content_element = html.xpath('//div[contains(@class, "art-content")]')
        assert len(content_element) == 1, 'news content should only have one'
        abs_path = helpers.cache_element(content_element[0], title)
        return {'source': self.source_name, 'title': title, 'date': cooked_date, 'path': abs_path}
