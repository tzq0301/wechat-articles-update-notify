import logging
import os

from email_sender import EmailSender
import schedule
from scrapy import Spider
import yaml

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    with open("application.yml", "r") as f:
        config = yaml.load(f, yaml.FullLoader)

    emailSender: EmailSender = EmailSender(
        mail_host=os.environ.get("MAIL_HOST"),
        mail_username=os.environ.get("MAIL_USERNAME"),
        mail_password=os.environ.get("MAIL_PASSWORD"),
        sender_email=os.environ.get("SENDER_EMAIL"),
        receiver_email=os.environ.get("RECEIVER_EMAIL"),
    )

    spider: Spider = Spider(config["service_ids"], emailSender)

    schedule.every(5).minutes.do(spider.refresh)
    while True:
        schedule.run_pending()
