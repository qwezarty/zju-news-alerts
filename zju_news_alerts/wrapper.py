# -*- coding: utf-8 -*-

"""
    zju_news_alerts.wrapper
    ~~~~~~~~~~~~~~~~~~~~~
    Here lies all the decorators.
    :author: qwezarty
    :date: 11:41 am Aug 8 2019
    :email: qwezarty@gmail.com
"""

import os
import smtplib
from email.message import EmailMessage

def mail_errors(func):
    def mail_errors_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as error:
            msg = EmailMessage()
            msg["Subject"] = "error occoured in zna"
            msg["Subject"] = "hello world"
            msg["From"] = "zju.news.alerts@outlook.com"
            msg["To"] = "qwezarty@gmail.com"
            # msg["Content-type"] = "text/html"
            msg.set_content(str(error))
            with smtplib.SMTP('smtp.office365.com', 587) as s:
                s.starttls()
                s.login("zju.news.alerts@outlook.com", os.environ["ZJU_PASS"])
                s.send_message(msg)
    return mail_errors_wrapper

