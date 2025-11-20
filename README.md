# 🎅 Secret Santa Local Email Sender

Secret Santa Local Email Sender is a program for those who want to organise a secret santa
but do not want to leak a list of email addresses to an online tool.

The program connects to your SMTP TLS server and send the emails for you, from your email address.

# Usage

- Fill the `SMTP_HOST`, `LOGIN_ACCOUNT` and `SENDER_ACCOUNT` variables in `email_sender.py`
- Create a `password.py` file that contains `PASSWORD='your_email_password'`
- Create a `participants.txt` file that contains the list of your participants in format:
```
Michael Scott,michael.scott@dundermifflin.com
Dwight Schrute,dwight-schrute@bearbeetsbattlestargalactica.us
Ryan Howard,ryan@dm-infinity.io
```
- Run `secret_santa.py`
- Each participant will receive an email with the name of their lucky colleague
- A `assignations.txt` file will be generated, containing the assignations
- The next year, you can rename that file to `previous_assignations.txt` and the script will make sure that the same
gifter-giftee combination does not happen again


