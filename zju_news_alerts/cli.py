# -*- coding: utf-8 -*-

"""
    zju_news_alerts.cli
    ~~~~~~~~~~~~~~~~~~~~~
    A simple command line application to run zju_news_alerts.
    :author: qwezarty
    :date: 02:48 pm Jul 17 2019
    :email: qwezarty@gmail.com
"""

import sys
import argparse
from zju_news_alerts.app import App

def _parse_args():
    """return a parser with arguments and values"""
    parser = argparse.ArgumentParser()

    _init_general_parsers(parser)
    _init_subparsers(parser)

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    return parser.parse_args()

def _init_general_parsers(parser):
    """initialize global cli arguments"""
    parser.add_argument(
        '-v', '--version',
        action = 'version',
        version = '%(prog)s 0.0.1',
        help = 'show version and exit.'
    )

def _init_subparsers(parent):
    """initialize cli sub-positional arguments"""
    subparsers = parent.add_subparsers()
    # serve
    parser_serve = subparsers.add_parser(
        'serve',
        help = 'starting server.'
    )
    parser_serve.set_defaults(func=serve)
    # list
    parser_list = subparsers.add_parser(
        'list',
        help = 'list no.1 page of source'
    )
    parser_list.set_defaults(func=list)
    parser_list.add_argument(
        "source",
        help = "the source you want to list"
    )
    # get
    parser_get = subparsers.add_parser(
        'get',
        help = 'get the latest post of source'
    )
    parser_get.set_defaults(func=get)
    parser_get.add_argument(
        "source",
        help = "the source you want to get"
    )
    # mail
    parser_mail = subparsers.add_parser(
        'mail',
        help = 'get the latest post of source'
    )
    parser_mail.set_defaults(func=mail)
    parser_mail.add_argument(
        "source",
        help = "the source you want to get"
    )

app = App(__name__)

def serve(args):
    app.serve()

def list(args):
    rets = app.source(args.source).list()
    print(rets)

def get(args):
    ret = app.source(args.source).get()
    print(ret)

def mail(args):
    app.source(args.source)
    app.send()

def main():
    print('welcome to use zju-news-alerts cli tool!')
    args = _parse_args()
    if hasattr(args, 'func'):
        args.func(args)
