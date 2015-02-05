=====
Usage
=====

.. doctest::

To use Python Salvitobot in a project::

    >>> import salvitobot

    >>> bot = salvitobot.Bot()
    >>> bot.get_quake(country='Peru')  # find earthquake records for Peru

    >>> if bot.quake is not None and bot.is_new_quake is True:
    ...     bot.tweet()
    ...     bot.write_post()
