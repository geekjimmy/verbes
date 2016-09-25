from django.apps import AppConfig

class AppConfig(AppConfig):
    name = 'apps.verbes'

    def ready(self):
        import apps.verbes.signals
