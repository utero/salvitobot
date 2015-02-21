from salvitobot import Bot


def main():
    bot = Bot()
    bot.get_quake(country='Indonesia')
    if bot.is_new_quake():
        bot.write_stories()
        # bot.post_to_wp()
        bot.tweet()
        # bot.send_email_to(['myemailaccount@gmail.com'])


if __name__ == "__main__":
    main()
