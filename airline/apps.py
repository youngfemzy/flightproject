from django.apps import AppConfig


class AirlineConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'airline'

    # ONCE THIS APPLICATION IS LOADED , CALL SIGNALS.PY , TO SET ALL USERS AS A CUSTOMER
    def ready(self):
        import airline.signals
