import logging
from typing import List

from email.mime.text import MIMEText
import smtplib
from smtplib import SMTP


class EmailSender:
    def __init__(self, mail_host: str, mail_username: str, mail_password: str,
                 sender_email: str, receiver_email: str) -> None:
        if not (mail_host and mail_username and mail_password and sender_email and receiver_email):
            logging.error(f"EmailSender 初始化失败：mail_host={mail_host}，"
                          f"mail_username={mail_username}，mail_password={mail_password}，"
                          f"sender_email={sender_email}，receiver_email={receiver_email}")
            exit(1)
        self._mail_host: str = mail_host
        self._mail_username: str = mail_username
        self._mail_password: str = mail_password
        self._sender_email: str = sender_email
        self._receiver_email: str = receiver_email
        logging.info("EmailSender 初始化成功")

    def __call__(self, subject: str, content: str) -> None:
        message: MIMEText = MIMEText(content, 'html', 'utf-8')
        message.add_header('From', self._sender_email)
        message.add_header('To', self._receiver_email)
        message.add_header('Subject', subject)
        message.add_header('Content_Disposition', 'attachment; filename="info.html"')

        try:
            smtp_object: SMTP = SMTP()
            smtp_object.connect(host=self._mail_host, port=25)
            smtp_object.login(user=self._mail_username, password=self._mail_password)
            smtp_object.sendmail(self._sender_email, [self._receiver_email], message.as_string())
            smtp_object.quit()
            logging.info(f"发送邮件成功")
        except smtplib.SMTPException as e:
            logging.error("发送邮件出错: ", e)
