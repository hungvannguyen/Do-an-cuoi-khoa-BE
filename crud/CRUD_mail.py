from mail.mail import send_mail

from mail.template import template


def create_auto_mail(mail_to, title, content):
    return send_mail(mail_to=mail_to, title=title, content=template)
