from email import message
import email
import smtplib
from email.mime.text import MIMEText

def send_mail(username, dealer, rating, comment):
    port = 2525
    smtp_server = 'smtp.mailtrap.io'
    login = '27ee2f8ee77026'
    password = '04f95fac592852'
    message = f"<h3>New feedback has received!!<ul><li>{username}</li><li>{dealer}</li><li>{rating}</li><li>{comment}</li></ul></h3>"

    sender_email = 'harshavardhanak@gmail.com'
    receiver_email = 'harshakhv57@gmail.com'
    msg = MIMEText(message, 'html')
    msg['SUBJECT'] = 'Customer service feedback'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    #send mail
    with smtplib.SMTP(smtp_server, port) as server:
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())