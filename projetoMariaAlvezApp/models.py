from django.db import models
from django.core.exceptions import ValidationError
from django.utils.timezone import now

class Consulta(models.Model):
    id_consulta = models.BigAutoField(primary_key=True)
    animal = models.ForeignKey('Animal', on_delete=models.CASCADE)
    veterinario = models.CharField(max_length=100, help_text="Nome do veterinário responsável")
    data_consulta = models.DateTimeField(default=now, help_text="Data e hora da consulta")
    
    # Sinais Vitais
    frequencia_cardiaca = models.PositiveIntegerField(help_text="Frequência Cardíaca (bpm)")
    frequencia_respiratoria = models.PositiveIntegerField(help_text="Frequência Respiratória (rpm)")
    temperatura = models.DecimalField(max_digits=4, decimal_places=1, help_text="Temperatura (°C)")
    peso = models.DecimalField(max_digits=5, decimal_places=2, help_text="Peso do animal (kg)")
    avaliacao_mucosa = models.TextField(help_text="Descrição da avaliação de mucosa")

    # Observações gerais
    queixa_principal = models.TextField(help_text="Queixa principal apresentada pelo tutor")
    historico_clinico = models.TextField(help_text="Histórico clínico do animal")
    exame_clinico = models.TextField(help_text="Resultados do exame clínico", blank=True, null=True)

    # Diagnóstico e Tratamento
    diagnostico = models.TextField(help_text="Diagnóstico", blank=True, null=True)
    tratamento = models.TextField(help_text="Plano de tratamento", blank=True, null=True)
    medicamentos_prescritos = models.ManyToManyField('Medicamento', blank=True, help_text="Medicamentos prescritos")
    exames_solicitados = models.ManyToManyField('Exame', blank=True, help_text="Exames solicitados")

    # Outros detalhes
    observacoes = models.TextField(blank=True, null=True, help_text="Observações adicionais")
    data_registro = models.DateTimeField(auto_now_add=True)

    def clean(self):
        super().clean()
        if self.frequencia_cardiaca <= 0:
            raise ValidationError("Frequência Cardíaca deve ser maior que zero.")
        if self.frequencia_respiratoria <= 0:
            raise ValidationError("Frequência Respiratória deve ser maior que zero.")
        if self.temperatura <= 0:
            raise ValidationError("Temperatura deve ser maior que zero.")
        if self.peso <= 0:
            raise ValidationError("Peso deve ser maior que zero.")

    def __str__(self):
        return f"Consulta de {self.animal.nome} em {self.data_consulta.strftime('%d/%m/%Y %H:%M')}"

# Outros modelos necessários para relacionamentos, caso ainda não estejam definidos
class Medicamento(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()

    def __str__(self):
        return self.nome

class Exame(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()

    def __str__(self):
        return self.nome

class Animal(models.Model):
    nome = models.CharField(max_length=100)
    tutor = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

# Create your models here.
