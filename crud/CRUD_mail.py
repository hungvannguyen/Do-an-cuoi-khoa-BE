from mail.mail import send_mail


def create_auto_mail(mail_to, title, content):
    return send_mail(mail_to=mail_to, title=title, content=content)
