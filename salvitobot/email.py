import smtplib


def send(email_receivers, stories):
    sender = 'salvitobot@salvitobot.com'

    for story in stories:
        message = ''

        message += "From: Salvitobot <" + sender + ">\n"
        message += "To: <" + '><'.join(email_receivers) + ">\n"
        message += "Subject: " + story['title'] + "\n\n"

        message += story['body'] + "\n"

        try:
            smtpObj = smtplib.SMTP('localhost')
            smtpObj.sendmail(sender, email_receivers, message.encode('utf-8'))
            print("Successfully sent email. Probably it went to your SPAM folder.")
        except smtplib.SMTPException:
            print("Error: unable to send email")
