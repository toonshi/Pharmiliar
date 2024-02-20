from django.apps import AppConfig

class HospitalsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hospitals'

    def ready(self):
        from .location import run_script
        run_script()
