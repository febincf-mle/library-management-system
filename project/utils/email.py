import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email configuration
def send_email(receiver, subject, message_):

    sender_email = "febin.web3dev@gmail.com"
    password = "sqxbubebqaqawrwy"

    # Construct the email message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver
    message["Subject"] = subject
    body = message_
    message.attach(MIMEText(body, "plain"))

    # Connect to Gmail's SMTP server
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        # Log in to your Gmail account
        server.login(sender_email, password)
        # Send the email
        server.sendmail(sender_email, receiver, message.as_string())


