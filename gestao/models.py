import re
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinValueValidator
from django.utils import timezone
from validate_docbr import CPF
from dateutil.relativedelta import relativedelta

def valida_cpf(cpf):
    validador = CPF()
    return validador.validate(cpf)

def get_current_date():
    return timezone.now().date()

class Tutor(models.Model):
    cpf = models.CharField(
        max_length=14,
        unique=True,
        validators=[RegexValidator(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', 'Digite um CPF no formato 123.456.789-00.')]
    )
    nome = models.CharField(max_length=50)
    sobrenome = models.CharField(max_length=50)
    data_nascimento = models.DateField()
    email = models.EmailField(max_length=100, blank=True)
    cep = models.CharField(
        max_length=9,
        validators=[RegexValidator(r'^\d{5}-\d{3}$', 'Digite um CEP no formato 12345-678.')]
    )
    endereco = models.CharField(max_length=255)
    telefone = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\(\d{2}\)\s\d{4,5}-\d{4}$', 'Digite um telefone no formato (11) 91234-5678.')]
    )
    estado = models.CharField(max_length=2, blank=True, help_text="Sigla do estado (ex.: SP)")
    cidade = models.CharField(max_length=100, blank=True)
    data_nascimento = models.DateField()

    def clean(self):
        super().clean()
        if self.cpf:
            self.cpf = re.sub(r'\D', '', self.cpf)
            if len(self.cpf) != 11:
                raise ValidationError({'cpf': 'O CPF deve conter 11 dígitos.'})
            if not valida_cpf(self.cpf):
                raise ValidationError({'cpf': 'O CPF informado é inválido.'})
        if self.cep:
            self.cep = re.sub(r'\D', '', self.cep)
            if len(self.cep) != 8:
                raise ValidationError({'cep': 'O CEP deve conter 8 dígitos.'})
        if self.telefone:
            self.telefone = re.sub(r'\D', '', self.telefone)
            if len(self.telefone) < 10 or len(self.telefone) > 11:
                raise ValidationError({'telefone': 'O telefone deve conter 10 ou 11 dígitos.'})
        if self.data_nascimento:
            hoje = timezone.now().date()
            idade = relativedelta(hoje, self.data_nascimento).years
            if idade < 18:
                raise ValidationError({'data_nascimento': 'O tutor deve ter pelo menos 18 anos.'})
        if self.estado and len(self.estado) != 2:
            raise ValidationError({'estado': 'O estado deve ter exatamente 2 caracteres (ex.: SP).'})
    def nome_completo(self):
        return f"{self.nome} {self.sobrenome}"

    def __str__(self):
        return self.nome_completo()

    class Meta:
        indexes = [
            models.Index(fields=['cpf'], name='tutor_cpf_idx'),
            models.Index(fields=['nome', 'sobrenome'], name='tutor_nome_idx'),
        ]

class Especie(models.Model):
    id_especie = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=80)

    class Meta:
        verbose_name = "Espécie"
        verbose_name_plural = "Espécies"

    def __str__(self):
        return self.nome

    def clean(self):
        super().clean()
        if not self.nome.strip():
            raise ValidationError({'nome': 'O nome da espécie não pode estar vazio.'})

class Raca(models.Model):
    id_raca = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=80)
    especie = models.ForeignKey(Especie, on_delete=models.CASCADE, related_name="racas")

    class Meta:
        verbose_name = "Raça"
        verbose_name_plural = "Raças"

    def __str__(self):
        return self.nome

    def clean(self):
        super().clean()
        if not self.nome.strip():
            raise ValidationError({'nome': 'O nome da raça não pode estar vazio.'})

class Animal(models.Model):
    id_animal = models.BigAutoField(primary_key=True, verbose_name="ID do Animal")
    nome = models.CharField(
        max_length=80,
        verbose_name="Nome",
        blank=False,
        help_text="Nome do animal (máximo 80 caracteres)"
    )
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, verbose_name="Tutor", related_name="animais")
    raca = models.ForeignKey(Raca, on_delete=models.CASCADE, verbose_name="Raça", related_name="animais")
    idade = models.IntegerField(
        verbose_name="Idade",
        validators=[MinValueValidator(0, "A idade deve ser maior ou igual a 0")]
    )
    especie = models.ForeignKey(Especie, on_delete=models.CASCADE, verbose_name="Espécie", related_name="animais")
    data_cadastro = models.DateField(
        verbose_name="Data de Cadastro",
        default=get_current_date,
        help_text="Data em que o animal foi cadastrado"
    )

    class Meta:
        verbose_name = "Animal"
        verbose_name_plural = "Animais"
        indexes = [
            models.Index(fields=['nome'], name='animal_nome_idx'),
            models.Index(fields=['tutor'], name='animal_tutor_idx'),
            models.Index(fields=['especie'], name='animal_especie_idx'),
        ]

    def __str__(self):
        return self.nome

    def clean(self):
        super().clean()
        if not self.nome.strip():
            raise ValidationError({'nome': 'O nome do animal não pode estar vazio.'})
        if self.idade < 0:
            raise ValidationError({'idade': 'A idade do animal não pode ser negativa.'})
        if not self.tutor:
            raise ValidationError({'tutor': 'Um animal deve ter um tutor associado.'})
        if not self.raca or not self.especie:
            raise ValidationError({'raca': 'Raça e espécie são obrigatórios.', 'especie': 'Raça e espécie são obrigatórios.'})
        if self.data_cadastro > timezone.now().date():
            raise ValidationError({'data_cadastro': 'A data de cadastro não pode ser no futuro.'})

    @property
    def idade_em_meses(self):
        hoje = timezone.now().date()
        delta = relativedelta(hoje, self.data_cadastro)
        return max(0, delta.years * 12 + delta.months)

    def eh_valido(self):
        return self.idade >= 0 and self.tutor is not None

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('animal-detail', kwargs={'pk': self.pk})

class Vacina(models.Model):
    id_vacina = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    especie = models.ForeignKey(Especie, on_delete=models.CASCADE, related_name="vacinas")
    dose = models.CharField(max_length=50)
    intervalo = models.IntegerField(help_text="Intervalo em meses", validators=[MinValueValidator(1)])
    fabricante = models.CharField(max_length=100)
    lote = models.CharField(max_length=50)
    validade = models.DateField()
    custo = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    recomendacoes = models.TextField(blank=True, null=True)
    data_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Vacina"
        verbose_name_plural = "Vacinas"

    def __str__(self):
        return self.nome

    def clean(self):
        super().clean()
        if not self.nome.strip():
            raise ValidationError({'nome': 'O nome da vacina não pode estar vazio.'})
        if self.validade < timezone.now().date():
            raise ValidationError({'validade': 'A validade não pode ser no passado.'})

class Medicamento(models.Model):
    id_medicamento = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    quantidade = models.IntegerField(validators=[MinValueValidator(0)])
    descricao = models.TextField()
    principio_ativo = models.CharField(max_length=100)
    indicacao = models.TextField()
    contraindicacoes = models.TextField(blank=True, null=True)
    dose = models.CharField(max_length=50)
    administracao = models.CharField(
        max_length=50,
        choices=[
            ('Oral', 'Oral'),
            ('Injetável', 'Injetável'),
            ('Tópico', 'Tópico'),
        ],
        default='Oral'
    )
    fabricante = models.CharField(max_length=100)
    estoque = models.IntegerField(validators=[MinValueValidator(0)])
    preco = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    validade = models.DateField()
    data_registro = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Medicamento"
        verbose_name_plural = "Medicamentos"

    def __str__(self):
        return self.nome

    def clean(self):
        super().clean()
        if not self.nome.strip():
            raise ValidationError({'nome': 'O nome do medicamento não pode estar vazio.'})
        if self.validade < timezone.now().date():
            raise ValidationError({'validade': 'A validade não pode ser no passado.'})

class Exame(models.Model):
    id_exame = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    tipo = models.CharField(max_length=50, choices=[
        ('Imagem', 'Imagem'),
        ('Laboratorial', 'Laboratorial'),
        ('Clínico', 'Clínico'),
    ])
    especie = models.ForeignKey(Especie, on_delete=models.CASCADE, related_name="exames")
    preco = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    equipamento = models.CharField(max_length=100, blank=True, null=True)
    duracao = models.DurationField(help_text="Duração média do exame (hh:mm:ss)")
    recomendacoes_pre = models.TextField(blank=True, null=True)
    data_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Exame"
        verbose_name_plural = "Exames"

    def __str__(self):
        return self.nome

    def clean(self):
        super().clean()
        if not self.nome.strip():
            raise ValidationError({'nome': 'O nome do exame não pode estar vazio.'})

class Prestadores(models.Model):
    id_prestador = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Prestador"
        verbose_name_plural = "Prestadores"

    def __str__(self):
        return self.nome

    def clean(self):
        super().clean()
        if not self.nome.strip():
            raise ValidationError({'nome': 'O nome do prestador não pode estar vazio.'})

class VacinaVermifugos(models.Model):
    id_vacina_vermifugo = models.BigAutoField(primary_key=True)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name="vacinas_vermifugos")
    tipo = models.CharField(max_length=50)
    data_aplicacao = models.DateField()
    data_proximo_reforco = models.DateField(blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Vacina/Vermífugo"
        verbose_name_plural = "Vacinas/Vermífugos"

    def __str__(self):
        return f"{self.animal.nome} - {self.tipo}"

    def clean(self):
        super().clean()
        if not self.tipo.strip():
            raise ValidationError({'tipo': 'O tipo não pode estar vazio.'})
        if self.data_aplicacao > timezone.now().date():
            raise ValidationError({'data_aplicacao': 'A data de aplicação não pode ser no futuro.'})
        if self.data_proximo_reforco and self.data_proximo_reforco < self.data_aplicacao:
            raise ValidationError({'data_proximo_reforco': 'A data do próximo reforço não pode ser anterior à data de aplicação.'})

    def calcular_proximo_reforco(self):
        if self.data_aplicacao:
            self.data_proximo_reforco = self.data_aplicacao + relativedelta(months=1)
            self.save()

class AnimalCastracao(models.Model):
    id_castracao = models.BigAutoField(primary_key=True)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name="castracoes")
    posicao_fila = models.IntegerField(validators=[MinValueValidator(1)])
    data_cadastro = models.DateField(default=get_current_date)
    status_castracao = models.CharField(max_length=20, choices=[('Pendente', 'Pendente'), ('Realizada', 'Realizada')])
    data_prevista_castracao = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = "Animal para Castração"
        verbose_name_plural = "Animais para Castração"

    def __str__(self):
        return f"{self.animal.nome} - {self.status_castracao}"

    def clean(self):
        super().clean()
        if self.data_prevista_castracao and self.data_cadastro:
            if self.data_prevista_castracao < self.data_cadastro:
                raise ValidationError({'data_prevista_castracao': 'A data prevista para castração não pode ser anterior à data de cadastro.'})
        if self.data_cadastro > timezone.now().date():
            raise ValidationError({'data_cadastro': 'A data de cadastro não pode ser no futuro.'})

class ListaCastracao(models.Model):
    id_lista = models.BigAutoField(primary_key=True)
    animais = models.ManyToManyField(AnimalCastracao, related_name="listas_castracao")
    nome_lista = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Lista de Castração"
        verbose_name_plural = "Listas de Castração"

    def __str__(self):
        return self.nome_lista

    def clean(self):
        super().clean()
        if not self.nome_lista.strip():
            raise ValidationError({'nome_lista': 'O nome da lista não pode estar vazio.'})

class ExameVeterinario(models.Model):
    id_exame_vet = models.BigAutoField(primary_key=True)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name="exames_veterinarios")
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name="exames_veterinarios")
    tipo_exame = models.CharField(max_length=50)
    data_exame = models.DateField()
    veterinario_solicitante = models.CharField(max_length=100)
    resultados = models.TextField(blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Exame Veterinário"
        verbose_name_plural = "Exames Veterinários"

    def __str__(self):
        return f"{self.animal.nome} - {self.tipo_exame}"

    def clean(self):
        super().clean()
        if not self.tipo_exame.strip():
            raise ValidationError({'tipo_exame': 'O tipo de exame não pode estar vazio.'})
        if self.data_exame > timezone.now().date():
            raise ValidationError({'data_exame': 'A data do exame não pode ser no futuro.'})

class ListaExames(models.Model):
    id_lista_exames = models.BigAutoField(primary_key=True)
    exames = models.ManyToManyField(ExameVeterinario, related_name="listas_exames")
    nome_lista = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Lista de Exames"
        verbose_name_plural = "Listas de Exames"

    def __str__(self):
        return self.nome_lista

    def clean(self):
        super().clean()
        if not self.nome_lista.strip():
            raise ValidationError({'nome_lista': 'O nome da lista não pode estar vazio.'})

class Produto(models.Model):
    id_produto = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    quantidade = models.IntegerField(validators=[MinValueValidator(0)])
    validade = models.DateField()
    fornecedor = models.CharField(max_length=100)
    quantidade_minima = models.IntegerField(validators=[MinValueValidator(0)])
    data_ultima_reposicao = models.DateField()

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"

    def __str__(self):
        return self.nome

    def clean(self):
        super().clean()
        if not self.nome.strip():
            raise ValidationError({'nome': 'O nome do produto não pode estar vazio.'})
        if self.validade < timezone.now().date():
            raise ValidationError({'validade': 'A validade não pode ser no passado.'})
        if self.data_ultima_reposicao > timezone.now().date():
            raise ValidationError({'data_ultima_reposicao': 'A data da última reposição não pode ser no futuro.'})

    def precisa_repor(self):
        return self.quantidade < self.quantidade_minima

class Estoque(models.Model):
    id_estoque = models.BigAutoField(primary_key=True)
    produtos = models.ManyToManyField(Produto, related_name="estoques")
    nome_estoque = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Estoque"
        verbose_name_plural = "Estoques"

    def __str__(self):
        return self.nome_estoque

    def clean(self):
        super().clean()
        if not self.nome_estoque.strip():
            raise ValidationError({'nome_estoque': 'O nome do estoque não pode estar vazio.'})

class Cirurgia(models.Model):
    id_cirurgia = models.BigAutoField(primary_key=True)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name="cirurgias")
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name="cirurgias")
    tipo_cirurgia = models.CharField(max_length=100)
    veterinario = models.CharField(max_length=100)
    responsavel = models.CharField(max_length=100)
    data_cirurgia = models.DateField()
    observacoes = models.TextField(blank=True, null=True)
    pos_cirurgicas = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Cirurgia"
        verbose_name_plural = "Cirurgias"

    def __str__(self):
        return f"{self.animal.nome} - {self.tipo_cirurgia}"

    def clean(self):
        super().clean()
        if not self.tipo_cirurgia.strip():
            raise ValidationError({'tipo_cirurgia': 'O tipo de cirurgia não pode estar vazio.'})
        if self.data_cirurgia > timezone.now().date():
            raise ValidationError({'data_cirurgia': 'A data da cirurgia não pode ser no futuro.'})

class Internacao(models.Model):
    id_internacao = models.BigAutoField(primary_key=True)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name="internacoes")
    motivo_internacao = models.TextField()
    data_entrada = models.DateField()
    data_saida = models.DateField(blank=True, null=True)
    status_recuperacao = models.CharField(max_length=50)
    observacoes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Internação"
        verbose_name_plural = "Internações"

    def __str__(self):
        return f"{self.animal.nome} - {self.motivo_internacao}"

    def clean(self):
        super().clean()
        if not self.motivo_internacao.strip():
            raise ValidationError({'motivo_internacao': 'O motivo da internação não pode estar vazio.'})
        if self.data_entrada > timezone.now().date():
            raise ValidationError({'data_entrada': 'A data de entrada não pode ser no futuro.'})
        if self.data_saida and self.data_saida < self.data_entrada:
            raise ValidationError({'data_saida': 'A data de saída não pode ser anterior à data de entrada.'})

class ConsultaClinica(models.Model):
    id_consulta = models.BigAutoField(primary_key=True)
    motivo_atendimento = models.TextField()
    valor_consulta = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    valor_medicamentos = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    observacoes = models.TextField(blank=True, null=True)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name="consultas")
    data_hora = models.DateTimeField(
        verbose_name="Data e Hora da Consulta",
        default=timezone.now
    )

    class Meta:
        verbose_name = "Consulta Clínica"
        verbose_name_plural = "Consultas Clínicas"

    def __str__(self):
        return f"Consulta {self.id_consulta} - {self.tutor}"

    def clean(self):
        super().clean()
        if not self.motivo_atendimento.strip():
            raise ValidationError({'motivo_atendimento': 'O motivo do atendimento não pode estar vazio.'})
        if self.data_hora > timezone.now():
            raise ValidationError({'data_hora': 'A data e hora da consulta não podem ser no futuro.'})

    def calcular_total(self):
        return self.valor_consulta + self.valor_medicamentos

class RelatorioAtendimento(models.Model):
    id_relatorio = models.BigAutoField(primary_key=True)
    data_atendimento = models.DateField()
    hora_atendimento = models.TimeField()
    tipo_atendimento = models.CharField(max_length=50)
    vet_responsavel = models.CharField(max_length=100)
    diagnostico_inicial = models.TextField()
    observacoes = models.TextField(blank=True, null=True)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name="relatorios_atendimento")
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name="relatorios_atendimento")
    telefone_contato = models.CharField(
        max_length=11,
        validators=[RegexValidator(
            r'^\d{10,11}$',
            'Digite um número de telefone válido com 10 ou 11 dígitos.'
        )]
    )
    procedimento = models.TextField()
    medicamentos = models.TextField()
    dosagem = models.CharField(max_length=50)
    frequencia = models.CharField(max_length=50)
    orientacoes_tutor = models.TextField()
    data_retorno = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = "Relatório de Atendimento"
        verbose_name_plural = "Relatórios de Atendimento"

    def __str__(self):
        return f"Relatório {self.id_relatorio} - {self.animal.nome}"

    def clean(self):
        super().clean()
        if not self.tipo_atendimento.strip():
            raise ValidationError({'tipo_atendimento': 'O tipo de atendimento não pode estar vazio.'})
        if not self.diagnostico_inicial.strip():
            raise ValidationError({'diagnostico_inicial': 'O diagnóstico inicial não pode estar vazio.'})
        if not self.procedimento.strip():
            raise ValidationError({'procedimento': 'O procedimento não pode estar vazio.'})
        if self.data_atendimento > timezone.now().date():
            raise ValidationError({'data_atendimento': 'A data de atendimento não pode ser no futuro.'})
        if self.data_retorno and self.data_retorno < self.data_atendimento:
            raise ValidationError({'data_retorno': 'A data de retorno não pode ser anterior à data de atendimento.'})
        if self.telefone_contato:
            cleaned_telefone = re.sub(r'\D', '', self.telefone_contato)
            if len(cleaned_telefone) not in (10, 11):
                raise ValidationError({'telefone_contato': 'O telefone de contato deve ter 10 ou 11 dígitos.'})
            self.telefone_contato = cleaned_telefone

class RelatorioAcompanhamento(models.Model):
    id_acompanhamento = models.BigAutoField(primary_key=True)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name="relatorios_acompanhamento")
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name="relatorios_acompanhamento")
    data_atendimento = models.DateField()
    tipo_atendimento = models.CharField(max_length=50)
    vet_responsavel = models.CharField(max_length=100)
    diagnostico = models.TextField()
    observacoes = models.TextField(blank=True, null=True)
    procedimento = models.TextField()
    medicamentos = models.TextField()
    dosagem = models.CharField(max_length=50)
    frequencia = models.CharField(max_length=50)
    orientacoes_tutor = models.TextField()
    data_retorno = models.DateField(blank=True, null=True)
    tipo_vacina_exame = models.CharField(max_length=50)
    data_aplicacao_exame = models.DateField()
    data_prevista_proximo = models.DateField(blank=True, null=True)
    resultados_exames = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Relatório de Acompanhamento"
        verbose_name_plural = "Relatórios de Acompanhamento"

    def __str__(self):
        return f"Acompanhamento {self.id_acompanhamento} - {self.animal.nome}"

    def clean(self):
        super().clean()
        if not self.tipo_atendimento.strip():
            raise ValidationError({'tipo_atendimento': 'O tipo de atendimento não pode estar vazio.'})
        if not self.diagnostico.strip():
            raise ValidationError({'diagnostico': 'O diagnóstico não pode estar vazio.'})
        if not self.procedimento.strip():
            raise ValidationError({'procedimento': 'O procedimento não pode estar vazio.'})
        if self.data_atendimento > timezone.now().date():
            raise ValidationError({'data_atendimento': 'A data de atendimento não pode ser no futuro.'})
        if self.data_aplicacao_exame > timezone.now().date():
            raise ValidationError({'data_aplicacao_exame': 'A data de aplicação/exame não pode ser no futuro.'})
        if self.data_retorno and self.data_retorno < self.data_atendimento:
            raise ValidationError({'data_retorno': 'A data de retorno não pode ser anterior à data de atendimento.'})
        if self.data_prevista_proximo and self.data_prevista_proximo < self.data_aplicacao_exame:
            raise ValidationError({'data_prevista_proximo': 'A data prevista para o próximo exame não pode ser anterior à data de aplicação.'})