from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.decorators import task

from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings


@task
def send_email_users(email_li, msg):
    from_email = settings.EMAIL_HOST_USER
    to_email = email_li
    html = get_template("mail.html").render({'msg': msg})
    # html = f'<h1>{msg}</h1>'
    sub = 'Django test mail'
    send_mail(sub, "", from_email, to_email, html_message=html)
