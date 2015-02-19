=====
Usage
=====

.. doctest::

Encuentra sismos recientes para Perú::

    >>> from salvitobot import Bot
    >>> bot = Bot()
    >>> bot.get_quake(country='Peru')
    >>> bot.quake
    []

Encuentra sismos recientes para Venezuela::

    >>> bot.get_quake(country='Venezuela')
    >>> bot.quake
    [{'tz': -240,
    'depth': 72.38,
    'time': 1423173055590,
    'datetime_utc': datetime.datetime(2015, 2, 5, 21, 50, 55, 589999, tzinfo=<UTC>),
    'longitude': -62.0483,
    'tuit': 'SISMO. 4.7 grados mb en 58km NNE of Gueiria, Venezuela. A horas  http://earthquake.usgs.gov/earthquakes/eventpage/usc000tmka',
    'link': 'http://earthquake.usgs.gov/earthquakes/eventpage/usc000tmka',
    'type': 'earthquake',
    'place': '58km NNE of Gueiria, Venezuela',
    'magnitude': 4.7,
    'magnitude_type': 'mb',
    'code': 'c000tmka',
    'latitude': 11.0419}]]

Averigua si este sismo es nuevo y no está en la base de datos::

    >>> bot.is_new_quake()
    True

Ya que es nuevo, escribe un post pero no lo publiques aún::

    >>> bot.write_stories()
    <BLANKLINE>
    Un temblor de mediana magnitud de 4.7 grados tuvo
    lugar el 05 Feb, 2015 por la tarde a 58km NNE of Gueiria, Venezuela
    según el Servicio Geológico de EE.UU.
    El temblor se produjo a las 21:50 de la tarde,
    del Tiempo universal coordinado (UTC), a una profundidad de
    72.38 kilómetros.
    <BLANKLINE>
    Según el USGS, el epicentro se ubicó a 2 km al SW de Umuquena, y a 18 km al E de La Fria, Venezuela.
    <BLANKLINE>
    La información proviene del USGS Earthquake Notification Service. Este post
    fue elaborado por un algoritmo escrito por el autor.
    <BLANKLINE>

Publica el post en tu instalación de WordPress::

    >>> bot.post_to_wp()

Salvitobot intentará adiviar el URL de tu post::

    >>> bot.post_urls
    ['https://example.wordpress.com/2015/02/06/blah-blah/']

Si no quieres que Salvitobot postee automáticamente en tu blog de Wordpress,
puedes pedir a Salvitobot que te envíe la nota periodística a tu email::

    >>> bot.send_mail_to(['production@utero.pe', 'aniversarioperu1@gmail.com'])
