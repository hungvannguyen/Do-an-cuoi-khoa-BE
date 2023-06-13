from mail.mail import send_mail

from mail.template import template


def create_confirm_mail(mail_to):
    link = f"http://localhost:3000/email/confirm?email={mail_to}"
    text = template
    text = text.replace('<a href="http://dhsgundam3" class="es-button"', f'<a href="{link}" class="es-button"')
    return send_mail(mail_to=mail_to, title="[DhsGundam] Please confirm your Email!", content=text)
