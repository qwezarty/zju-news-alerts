# -*- coding: utf-8 -*-

import pytest
from dateutil.parser import parse
from zju_news_alerts.engine import Engine

mocks = [
    {
        "source": "physics",
        "title": "2019年秋季研究生新生报到须知",
        "date": parse("2019-07-16"),
        "url":"http://physics.zju.edu.cn/chinese/redir.php?catalog_id=12267&object_id=158641"
    },
    {
        "source": "physics",
        "title": "物理学系2019年统考硕士研究生拟录取名单公示",
        "date": parse("2019-03-12"),
        "url":"http://physics.zju.edu.cn/chinese/redir.php?catalog_id=12267&object_id=152239"
    },
    {
        "source": "physics",
        "title": "2019年物理学系博士研究生“申请-考核”制初审结果公示",
        "date": parse("2019-01-10"),
        "url":"http://physics.zju.edu.cn/chinese/redir.php?catalog_id=12267&object_id=151365"
    }
]

engine = Engine()
engine.start = parse("2019-03-01")

def test_filter_posts():
    # boundary value
    rets = engine._filter_posts([])
    assert len(rets) == 0
    rets = engine._filter_posts(None)
    assert len(rets) == 0
    # normal value
    rets = engine._filter_posts(mocks)
    assert len(rets) == 2, 'start date not working when filter posts'
    engine.posts.insert_one(mocks[1])
    rets = engine._filter_posts(mocks)
    assert len(rets) == 1, 'cannot filter replica date in db when filter posts'
    engine.posts.delete_one(mocks[1])

def test_with_more_infos():
    # boundary value
    rets = engine.with_more_infos([])
    assert len(rets) == 0
    rets = engine.with_more_infos(None)
    assert len(rets) == 0
    # normal value
    cooked_post = engine.with_more_infos(mocks[1])
    assert cooked_post["source"]["_id"]
    assert cooked_post["source"]["description"]

