import smtplib
from email.message import EmailMessage

from password import PASSWORD


class EmailSender:
    LOGIN_ACCOUNT = 'myaccount@outlook.com'
    SENDER_ACCOUNT = 'myaccount@outlook.com'
    SMTP_HOST = 'smtp.office365.com'

    def __init__(self):
        self.smtp = smtplib.SMTP(self.SMTP_HOST, port=587)

    def connect(self):
        self.smtp.ehlo()  # Send the extended hello to our server
        self.smtp.starttls()  # Tell server we want to communicate with TLS encryption
        self.smtp.login(self.LOGIN_ACCOUNT, PASSWORD)  # login to our email server

    def send_email(self, to: str, title: str, text_content: str, html_content):
        message = EmailMessage()
        message['Subject'] = title
        message['From'] = self.SENDER_ACCOUNT
        message['To'] = to

        message.set_content(text_content)
        message.add_alternative(html_content, subtype='html')

        self.smtp.sendmail(self.SENDER_ACCOUNT,
                           to,
                           message.as_string())

    def disconnect(self):
        # Close the connection
        self.smtp.quit()
