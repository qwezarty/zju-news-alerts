# -*- coding: utf-8 -*-

"""
    zju_news_alerts.mail
    ~~~~~~~~~~~~~~~~~~~~~
    Mail service.
    :author: qwezarty
    :date: 10:30 am Jul 19 2019
    :email: qwezarty@gmail.com
"""

import smtplib
import os
from email.message import EmailMessage
from email.mime.text import MIMEText

class Mail:
    def __init__(self, post):
        self.post = post

    def send(self):
        content = ''
        with open(self.post["path"], 'r') as f:
            content = f.read()
        msg = MIMEText(content, 'html')
        msg["Subject"] = self.post["title"]
        msg["From"] = "zju.news.alerts@outlook.com"
        # msg["To"] = "qwezarty@163.com"
        msg["Bcc"] = ", ".join(self.post["source"]["subscribers"])
        msg["Content-type"] = "text/html"
        # add html content
        with smtplib.SMTP('smtp.office365.com', 587) as s:
            s.starttls()
            s.login("zju.news.alerts@outlook.com", os.environ["ZJU_PASS"])
            s.send_message(msg)
