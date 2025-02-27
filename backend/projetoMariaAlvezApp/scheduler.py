from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime, timedelta
from .models import Medicamento
from django.core.mail import send_mail

def notificar_medicamentos_vencendo():
    vencendo_em_breve = Medicamento.objects.filter(
        validade__lte=datetime.now().date() + timedelta(days=30),
        validade__gte=datetime.now().date()
        
    )
    
    # Imprime os medicamentos vencendo SOMENTE PARA TESTE DE NOTIFICAÇÃO
    for medicamento in vencendo_em_breve:
        print(f"Medicamento: {medicamento.nome} - Vencendo em: {medicamento.validade}")
"""
    for medicamento in vencendo_em_breve:
        send_mail(
            subject="Aviso: Medicamento vencendo em breve",
            message=f"O medicamento '{medicamento.nome}' vence em {medicamento.validade}.",
            from_email="monteirofp1985@gmail.com",
            recipient_list=["monteirofp1985@gmail.com"],
        )

def iniciar_agendamento():
    print("Método iniciar_agendamento chamado.")
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        notificar_medicamentos_vencendo,
        trigger=IntervalTrigger(days=1),  # Executa uma vez por dia
        id="notificar_medicamentos",  # Identificador único da tarefa
        replace_existing=True,  # Substitui a tarefa se ela já existir
    )
    scheduler.start()
    print("Agendamento iniciado!")
"""
