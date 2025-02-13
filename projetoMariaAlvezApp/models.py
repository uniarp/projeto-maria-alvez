from validate_docbr import CPF
from django.core.exceptions import ValidationError
from django.db import models

class Tutor(models.Model):
    id_tutor = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=80)
    sobrenome = models.CharField(max_length=80)
    rua = models.CharField(max_length=80)
    bairro = models.CharField(max_length=80)
    numero = models.IntegerField()
    cidade = models.CharField(max_length=80)
    estado = models.CharField(max_length=2)  # Exemplo: SP, RJ
    cep = models.CharField(max_length=9)
    email = models.CharField(max_length=60)
    telefone = models.CharField(max_length=15)
    cpf = models.CharField(max_length=14)
    def __str__(self):
        return f"{self.nome} {self.sobrenome} - {self.cpf}"

    def clean(self):
        super().clean()
        cpf_validator = CPF()
        if not cpf_validator.validate(self.cpf):
            raise ValidationError("O CPF informado é inválido.")

class Especie(models.Model):
    id_especie = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=80)

    def __str__(self):
        return self.nome

class Raca(models.Model):
    id_raca = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=80)
    especie = models.ForeignKey(Especie, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

class Animal(models.Model):
    id_animal = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=80)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    raca = models.ForeignKey(Raca, on_delete=models.CASCADE)
    idade = models.IntegerField()
    especie = models.ForeignKey(Especie, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

class Vacina(models.Model):
    id_vacina = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    especie = models.ForeignKey(Especie, on_delete=models.CASCADE)
    dose = models.CharField(max_length=50)
    intervalo = models.IntegerField(help_text="Intervalo em meses")
    fabricante = models.CharField(max_length=100)
    lote = models.CharField(max_length=50)
    validade = models.DateField()
    custo = models.DecimalField(max_digits=10, decimal_places=2)
    recomendacoes = models.TextField(blank=True, null=True)
    data_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Medicamento(models.Model):
    id_medicamento = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    principio_ativo = models.CharField(max_length=100)
    indicacao = models.TextField()
    contraindicacoes = models.TextField(blank=True, null=True)
    dose = models.CharField(max_length=50)
    administracao = models.CharField(max_length=50, choices=[
        ('Oral', 'Oral'),
        ('Injetável', 'Injetável'),
        ('Tópico', 'Tópico'),
    ])
    fabricante = models.CharField(max_length=100)
    estoque = models.IntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    validade = models.DateField()
    data_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Exame(models.Model):
    id_exame = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    tipo = models.CharField(max_length=50, choices=[
        ('Imagem', 'Imagem'),
        ('Laboratorial', 'Laboratorial'),
        ('Clínico', 'Clínico'),
    ])
    especie = models.ForeignKey(Especie, on_delete=models.CASCADE)  # Alterado para ForeignKey
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    equipamento = models.CharField(max_length=100, blank=True, null=True)
    duracao = models.DurationField(help_text="Duração média do exame (hh:mm:ss)")
    recomendacoes_pre = models.TextField(blank=True, null=True)
    data_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Prestadores(models.Model):

    pass