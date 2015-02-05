class Writer(object):
    """Writes blog posts and uploads to Wordpress.

    """
    def __init__(self):
        self.template = """
            Un {{ tremor }} de {{ magnitude_level }} magnitud de {{ magnitude_integer }} grados tuvo
            lugar el {{ date_local }} por la {{ time_of_day }} a {{ place }}
            según el Servicio Geológico de EE.UU.
            El {{ tremor }} se produjo a las {{ time }} de la {{ time_of_day }},
            del Tiempo universal coordinado (UTC), a una profundidad de
            {{ depth }} kilómetros.

            Según el USGS, el epicentro se ubicó a {{ related_place }}.
            """
        self.positive_historial_template = """
            En los últimos {{ days }} días, se han registrado {{ how_many }} temblores de magnitud 3,0
            o mayores en esta zona.
            """
        self.negative_historial_template = """
            En los últimos {{ days }} días, no se registraron temblores de magnitud 3,0 o mayores en esta
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
        print(items)
