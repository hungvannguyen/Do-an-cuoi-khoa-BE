from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import smtplib
import os

from sqlalchemy.orm import Session

from constants import Method, Target, Const
from crud import logger


def message(subject,
            text):
    # build message contents
    msg = MIMEMultipart()

    # Add Subject
    msg['Subject'] = subject

    # Add text contents
    msg.attach(MIMEText(text, 'html'))

    return msg


def send_mail(mail_to, title, content, db: Session):
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login('dhsgundam@gmail.com', 'morfwyqtzrovgvzy')
    msg = message(title, content)
    smtp.sendmail(from_addr="dhsgundam@gmail.com",
                  to_addrs=mail_to, msg=msg.as_string())
    # smtp.quit()

    return f"Email sent to {mail_to}"
