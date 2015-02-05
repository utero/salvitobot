import datetime
from datetime import timedelta as td
import re

from .wordpress import post_to_wp


class Writer(object):
    """Writes blog posts and uploads to Wordpress.

    """
    def __init__(self):
        self.template = """
            Un _tremor_ de _magnitude_level_ magnitud de _magnitude_integer_ grados tuvo
            lugar el _date_local_str_ por la _time_of_day1_ a _epicenter_
            según el Servicio Geológico de EE.UU.
            El _tremor_ se produjo a las _time_ de la _time_of_day2_,
            del Tiempo universal coordinado (UTC), a una profundidad de
            _depth_ kilómetros.

            Según el USGS, el epicentro se ubicó a _related_place_.
            """
        self.positive_historial_template = """
            En los últimos _days_ días, se han registrado _how_many_ temblores de magnitud 3.0
            o mayores en esta zona.
            """
        self.negative_historial_template = """
            En los últimos _days_ días, no se registraron temblores de magnitud 3.0 o mayores en esta
            zona.
            """
        self.template_footer = """
            La información proviene del USGS Earthquake Notification Service. Este post
            fue elaborado por un algoritmo escrito por el autor.
            """

    def write_post(self, items):
        """

        :param items: list of earthquake data (as dictionaries)
        """
        for item in items:
            print(item)
            if item['magnitude'] > 7.5:
                tremor = 'terremoto'
            else:
                tremor = 'temblor'

            if item['magnitude'] >= 7:
                magnitude_level = 'gran'
            elif 4 < item['magnitude'] < 7:
                magnitude_level = 'mediana'
            else:
                magnitude_level = 'escasa'

            magnitude_integer = str(item['magnitude'])
            date_local = item['datetime_utc'] + td(minutes=item['tz'])
            date_local_str = datetime.datetime.strftime(date_local, '%d %b, %Y')

            hour_of_day = int(datetime.datetime.strftime(date_local, '%H'))
            if 6 <= hour_of_day < 12:
                time_of_day1 = 'mañana'
            elif 12 <= hour_of_day < 18:
                time_of_day1 = 'tarde'
            elif 18 <= hour_of_day < 24:
                time_of_day1 = 'noche'
            elif hour_of_day == 24:
                time_of_day1 = 'madrugada'
            elif hour_of_day < 6:
                time_of_day1 = 'madrugada'

            epicenter = item['place']

            time = datetime.datetime.strftime(item['datetime_utc'], '%H:%M')
            if 6 <= hour_of_day < 12:
                time_of_day2 = 'mañana'
            elif 12 <= hour_of_day < 18:
                time_of_day2 = 'tarde'
            elif 18 <= hour_of_day < 24:
                time_of_day2 = 'noche'
            elif hour_of_day == 24:
                time_of_day2 = 'madrugada'
            elif hour_of_day < 6:
                time_of_day2 = 'madrugada'

            depth = str(item['depth'])

            text = self.template + "\n\n" + self.negative_historial_template + "\n\n"
            text += self.template_footer

            text = re.sub('_tremor_', tremor, text)
            text = re.sub('_magnitude_level_', magnitude_level, text)
            text = re.sub('_magnitude_integer_', magnitude_integer, text)
            text = re.sub('_date_local_str_', date_local_str, text)
            text = re.sub('_time_of_day1_', time_of_day1, text)
            text = re.sub('_time_of_day2_', time_of_day2, text)
            text = re.sub('_epicenter_', epicenter, text)
            text = re.sub('_time_', time, text)
            text = re.sub('_depth_', depth, text)

            title = 'Temblor gado ' + magnitude_integer + ' en ' + epicenter
            post_to_wp(title, text)
            print("Published post with title %s" % title)
