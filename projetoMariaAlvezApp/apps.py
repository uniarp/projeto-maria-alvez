from django.apps import AppConfig


class ProjetomariaalvezappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'projetoMariaAlvezApp'


class projetoMariaAlvezAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'projetoMariaAlvezApp'

    def ready(self):
        print("Método ready chamado.")
        # Importa e inicia o agendamento
        """from .scheduler import iniciar_agendamento
        iniciar_agendamento()
"""