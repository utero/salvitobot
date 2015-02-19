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
            message_to_user = "\nSuccessfully sent email.\n" \
                              "Probably it went to your SPAM folder.\n" \
                              "If you are using Gmail you might need to create a filter\n" \
                              "to avoid sending emails from <salvitobot@salvitobot.com> to \n" \
                              "your SPAM folder. More info here https://support.google.com/mail/answer/6579\n"
            print(message_to_user)
        except smtplib.SMTPException:
            print("Error: unable to send email")
