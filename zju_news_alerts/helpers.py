# -*- coding: utf-8 -*-

"""
    zju_news_alerts.helpers
    ~~~~~~~~~~~~~~~~~~~~~
    Implements various helpers.
    :author: qwezarty
    :date: 03:42 pm Jul 17 2019
    :email: qwezarty@gmail.com
"""

from pathlib import Path
import requests
from os import path, mkdir
from lxml import etree

root_path = Path(__file__).parent

def cache_response(response, name='last_response.html', encoding='utf-8'):
    """cache last response"""
    """located at cache/last_*_response.html"""
    if not isinstance(response, requests.Response):
        raise TypeError('cache response type only can be requests/Response')

    file_name = ''
    if response.status_code == 200:
        file_name = ''.join(['success_', name])
    else:
        file_name = ''.join(['error_', name])

    cache_dir = path.join(root_path, 'cache')
    if not path.exists(cache_dir):
        mkdir(cache_dir)
    abs_path = path.join(cache_dir, file_name)
    with open(abs_path, 'w+', encoding=encoding) as f:
        f.write(response.text.encode(response.encoding).decode(encoding, 'ignore'))
    return abs_path

def cache_element(element, file_name='last_artical.html'):
    tree = etree.ElementTree(element)
    cache_dir = path.join(root_path, 'cache')
    if not file_name.endswith('.html'):
        file_name = file_name + '.html'
    abs_path = path.join(cache_dir, file_name)
    tree.write(abs_path)
    return abs_path

def xpath_text(html, xpath, attr=''):
    """use xpath to get element's attribute from html"""
    """by default, it gets the text of node"""
    nodes = html.xpath(xpath)
    if len(nodes) != 1:
        cache_element(html, 'last_failed_xpath.html')
    assert len(nodes) == 1, 'node selected by xpath could only be 1'
    node = nodes[0]
    if attr == '':
        if hasattr(node, 'text'):
            return node.text
        return node
    else:
        return node.get(attr)

