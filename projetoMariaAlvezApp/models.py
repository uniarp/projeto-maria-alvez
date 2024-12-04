

# models.py
from django.db import models

class Medicamento(models.Model):
    nome = models.CharField(max_length=100)
    quantidade = models.PositiveIntegerField()
    validade = models.DateField()

    def __str__(self):
        return self.nome
