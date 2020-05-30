from django.apps import AppConfig


class MyappConfig(AppConfig):
    name = 'MyApp'

    def ready(self):
        import MyApp.signals
