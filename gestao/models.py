from validate_docbr import CPF
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import timedelta, date

class Tutor(models.Model):
    id_tutor = models.BigAutoField(primary_key=True, verbose_name="ID do Tutor")
    nome = models.CharField(max_length=80, verbose_name="Nome")
    sobrenome = models.CharField(max_length=80, verbose_name="Sobrenome")
    cpf = models.CharField(
        max_length=14,
        verbose_name="CPF",
        unique=True,
        validators=[RegexValidator(
            r'^\d{3}\.?\d{3}\.?\d{3}-?\d{2}$',
            'Digite um CPF válido no formato: 123.456.789-00.'
        )]
    )
    rg = models.CharField(
        max_length=9,
        verbose_name="RG",
        blank=True,
        validators=[RegexValidator(
            r'^\d{7,9}$',
            'Digite um RG válido com 7 a 9 dígitos.'
        )]
    )
    rua = models.CharField(max_length=80, verbose_name="Rua")
    bairro = models.CharField(max_length=80, verbose_name="Bairro")
    numero = models.IntegerField(verbose_name="Número", validators=[MinValueValidator(1)])
    cidade = models.CharField(max_length=80, verbose_name="Cidade")
    estado = models.CharField(max_length=2, verbose_name="Estado")
    cep = models.CharField(
        max_length=9,
        verbose_name="CEP",
        validators=[RegexValidator(
            r'^\d{5}[-.\s]?\d{3}$',
            'Digite um CEP válido no formato: 12345-678.'
        )]
    )
    email = models.EmailField(verbose_name="E-mail", blank=True)
    telefone = models.CharField(
        max_length=15,
        verbose_name="Telefone",
        blank=True,
        validators=[RegexValidator(
            r'^\+?55?\s?\(?[1-9]{2}\)?\s?\d{4,5}-?\d{4}$',
            'Digite um número de telefone válido no formato: +55 (DD) XXXXX-XXXX.'
        )]
    )
    cadastro_unico = models.BooleanField(default=False, verbose_name="Cadastro Único")
    data_cadastro = models.DateField(
        verbose_name="Data de Cadastro",
        default=timezone.now,
        help_text="Data em que o tutor foi cadastrado"
    )

    class Meta:
        verbose_name = "Tutor"
        verbose_name_plural = "Tutores"
        indexes = [
            models.Index(fields=['cpf'], name='tutor_cpf_idx'),
            models.Index(fields=['nome', 'sobrenome'], name='tutor_nome_idx'),
        ]

    def __str__(self):
        return f"{self.nome} {self.sobrenome} - {self.cpf}"

    def clean(self):
        super().clean()
        cpf_validator = CPF()
        cleaned_cpf = self.cpf.replace('.', '').replace('-', '')
        if not cpf_validator.validate(cleaned_cpf):
            raise ValidationError("O CPF informado é inválido.")
        if self.data_cadastro > timezone.now().date():
            raise ValidationError("A data de cadastro não pode ser no futuro.")
        self.cpf = cleaned_cpf

    @property
    def nome_completo(self):
        return f"{self.nome} {self.sobrenoha}"

    @property
    def endereco_completo(self):
        return f"{self.rua}, {self.numero}, {self.bairro}, {self.cidade} - {self.estado}, {self.cep}"

class Especie(models.Model):
    id_especie = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=80, unique=True)

    class Meta:
        verbose_name = "Espécie"
        verbose_name_plural = "Espécies"
        indexes = [models.Index(fields=['nome'], name='especie_nome_idx')]

    def __str__(self):
        return self.nome

class Raca(models.Model):
    id_raca = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=80)
    especie = models.ForeignKey(Especie, on_delete=models.CASCADE, related_name="racas")

    class Meta:
        verbose_name = "Raça"
        verbose_name_plural = "Raças"
        indexes = [models.Index(fields=['nome', 'especie'], name='raca_nome_idx')]
        unique_together = ['nome', 'especie']

    def __str__(self):
        return f"{self.nome} ({self.especie.nome})"

class Animal(models.Model):
    id_animal = models.IntegerField(unique=True, null=True, blank=True)  # Temporary null=True
    nome = models.CharField(max_length=100, verbose_name="Nome")
    especie = models.ForeignKey(
        Especie,
        on_delete=models.CASCADE,
        verbose_name="Espécie",
        related_name="animais",
        default=1
    )
    raca = models.ForeignKey(
        Raca,
        on_delete=models.CASCADE,
        verbose_name="Raça",
        related_name="animais",
        null=True,
        blank=True
    )
    cor = models.CharField(max_length=50, verbose_name="Cor")
    sexo = models.CharField(
        max_length=20,
        choices=[('M', 'Macho'), ('F', 'Fêmea')],
        verbose_name="Sexo"
    )
    idade = models.IntegerField(verbose_name="Idade", default=0)
    peso = models.FloatField(verbose_name="Peso")
    tutor = models.ForeignKey(
        Tutor,
        on_delete=models.CASCADE,
        verbose_name="Tutor",
        related_name="animais"
    )
    castrado = models.BooleanField(default=False, verbose_name="Castrado")
    disponivel_adocao = models.BooleanField(default=False, verbose_name="Disponível para adoção")
    data_cadastro = models.DateField(auto_now_add=True, verbose_name="Data de Cadastro")
    deficiencia = models.TextField(null=True, blank=True, verbose_name="Deficiência")

    class Meta:
        verbose_name = "Animal"
        verbose_name_plural = "Animais"

    def __str__(self):
        return self.nome

class Funcionario(models.Model):
    id_funcionario = models.BigAutoField(primary_key=True)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=255)
    cpf = models.CharField(
        max_length=14,
        unique=True,
        validators=[RegexValidator(
            r'^\d{3}\.?\d{3}\.?\d{3}-?\d{2}$',
            'Digite um CPF válido no formato: 123.456.789-00.'
        )]
    )
    rg = models.CharField(
        max_length=9,
        blank=True,
        validators=[RegexValidator(
            r'^\d{7,9}$',
            'Digite um RG válido com 7 a 9 dígitos.'
        )]
    )
    endereco = models.TextField()
    email = models.EmailField()
    telefone = models.CharField(
        max_length=15,
        validators=[RegexValidator(
            r'^\+?55?\s?\(?[1-9]{2}\)?\s?\d{4,5}-?\d{4}$',
            'Digite um número de telefone válido no formato: +55 (DD) XXXXX-XXXX.'
        )]
    )
    cargo = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Funcionário"
        verbose_name_plural = "Funcionários"
        indexes = [models.Index(fields=['cpf'], name='funcionario_cpf_idx')]

    def __str__(self):
        return self.nome

    def clean(self):
        super().clean()
        cpf_validator = CPF()
        cleaned_cpf = self.cpf.replace('.', '').replace('-', '')
        if not cpf_validator.validate(cleaned_cpf):
            raise ValidationError("O CPF informado é inválido.")
        self.cpf = cleaned_cpf

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
    custo = models.DecimalField(max_digits=10, decimal_places=2)
    recomendacoes = models.TextField(blank=True, null=True)
    data_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Vacina"
        verbose_name_plural = "Vacinas"
        indexes = [models.Index(fields=['nome', 'especie'], name='vacina_nome_idx')]

    def __str__(self):
        return f"{self.nome} ({self.especie.nome})"

    def clean(self):
        super().clean()
        if self.validade < timezone.now().date():
            raise ValidationError("A validade da vacina não pode ser no passado.")

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
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    validade = models.DateField()
    data_registro = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Medicamento"
        verbose_name_plural = "Medicamentos"
        indexes = [models.Index(fields=['nome'], name='medicamento_nome_idx')]

    def __str__(self):
        return self.nome

    def clean(self):
        super().clean()
        if self.validade < timezone.now().date():
            raise ValidationError("A validade do medicamento não pode ser no passado.")
        if self.preco < 0:
            raise ValidationError("O preço não pode ser negativo.")

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
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    equipamento = models.CharField(max_length=100, blank=True, null=True)
    duracao = models.DurationField(help_text="Duração média do exame (hh:mm:ss)")
    recomendacoes_pre = models.TextField(blank=True, null=True)
    data_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Exame"
        verbose_name_plural = "Exames"
        indexes = [models.Index(fields=['nome', 'especie'], name='exame_nome_idx')]

    def __str__(self):
        return f"{self.nome} ({self.especie.nome})"

    def clean(self):
        super().clean()
        if self.preco < 0:
            raise ValidationError("O preço não pode ser negativo.")
        if self.duracao <= timedelta(0):
            raise ValidationError("A duração deve ser maior que zero.")

class Prestadores(models.Model):
    id_prestador = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Prestador"
        verbose_name_plural = "Prestadores"
        indexes = [models.Index(fields=['nome'], name='prestador_nome_idx')]

    def __str__(self):
        return self.nome

class VacinaVermifugos(models.Model):
    id_vacina_vermifugo = models.BigAutoField(primary_key=True)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, verbose_name="Animal")
    tipo = models.CharField(max_length=50, choices=[
        ('Vacina', 'Vacina'),
        ('Vermífugo', 'Vermífugo'),
    ])
    data_aplicacao = models.DateField()
    data_proximo_reforco = models.DateField(blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Vacina/Vermífugo"
        verbose_name_plural = "Vacinas/Vermífugos"
        indexes = [models.Index(fields=['animal', 'tipo'], name='vacina_vermifugo_idx')]

    def __str__(self):
        return f"{self.animal.nome} - {self.tipo}"

    def clean(self):
        super().clean()
        if self.data_aplicacao > timezone.now().date():
            raise ValidationError("A data de aplicação não pode ser no futuro.")
        if self.data_proximo_reforco and self.data_proximo_reforco < self.data_aplicacao:
            raise ValidationError("A data do próximo reforço não pode ser anterior à data de aplicação.")

    def calcular_proximo_reforco(self):
        if self.data_aplicacao:
            intervalo = 30 if self.tipo == 'Vermífugo' else 365
            self.data_proximo_reforco = self.data_aplicacao + timedelta(days=intervalo)
            self.save()

class FilaCastracao(models.Model):
    STATUS_CHOICES = [
        ('AGUARDANDO', 'Aguardando'),
        ('REALIZADO', 'Realizado'),
        ('CANCELADO', 'Cancelado'),
    ]

    id_castracao = models.BigAutoField(primary_key=True)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, verbose_name="Animal", related_name="filas_castracao")
    posicao = models.IntegerField(validators=[MinValueValidator(1)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='AGUARDANDO')
    data_cadastro = models.DateField(default=timezone.now)
    data_prevista_castracao = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = "Fila de Castração"
        verbose_name_plural = "Filas de Castração"
        indexes = [models.Index(fields=['animal', 'status'], name='castracao_idx')]

    def clean(self):
        super().clean()
        if self.data_prevista_castracao and self.data_cadastro:
            if self.data_prevista_castracao < self.data_cadastro:
                raise ValidationError("A data prevista para castração não pode ser anterior à data de cadastro.")
        if self.data_cadastro > timezone.now().date():
            raise ValidationError("A data de cadastro não pode ser no futuro.")
        if self.status == 'REALIZADO':
            self.animal.castrado = True
            self.animal.save()

    def __str__(self):
        return f"Fila de castração para {self.animal.nome}"

class ListaCastracao(models.Model):
    id_lista = models.BigAutoField(primary_key=True)
    animais = models.ManyToManyField(FilaCastracao, related_name="listas")
    nome_lista = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Lista de Castração"
        verbose_name_plural = "Listas de Castração"
        indexes = [models.Index(fields=['nome_lista'], name='lista_castracao_idx')]

    def __str__(self):
        return self.nome_lista

class CandidatoAdocao(models.Model):
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('APROVADO', 'Aprovado'),
        ('REJEITADO', 'Rejeitado'),
    ]

    id_candidatura = models.BigAutoField(primary_key=True)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name='candidaturas_adocao')
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='candidaturas_adocao')
    data_candidatura = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDENTE')
    observacoes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Candidato à Adoção"
        verbose_name_plural = "Candidatos à Adoção"
        indexes = [models.Index(fields=['animal', 'status'], name='candidato_adocao_idx')]

    def __str__(self):
        return f"Candidatura de {self.tutor.nome_completo} para {self.animal.nome}"

    def clean(self):
        super().clean()
        if not self.animal.disponivel_adocao:
            raise ValidationError("O animal não está disponível para adoção.")
        if self.animal.tutor is not None and self.status == 'APROVADO':
            raise ValidationError("Animais com tutor não podem ser adotados.")

class ExameVeterinario(models.Model):
    id_exame_vet = models.BigAutoField(primary_key=True)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='exames_veterinarios')
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    tipo_exame = models.CharField(max_length=50)
    data_exame = models.DateField()
    veterinario_solicitante = models.CharField(max_length=100)
    resultados = models.TextField(blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Exame Veterinário"
        verbose_name_plural = "Exames Veterinários"
        indexes = [models.Index(fields=['animal', 'data_exame'], name='exame_vet_idx')]

    def __str__(self):
        return f"{self.animal.nome} - {self.tipo_exame}"

    def clean(self):
        super().clean()
        if self.data_exame > timezone.now().date():
            raise ValidationError("A data do exame não pode ser no futuro.")
        if self.tutor != self.animal.tutor and self.animal.tutor is not None:
            raise ValidationError("O tutor do exame deve ser o mesmo do animal.")

class ListaExames(models.Model):
    id_lista_exames = models.BigAutoField(primary_key=True)
    exames = models.ManyToManyField(ExameVeterinario, related_name="listas")
    nome_lista = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Lista de Exames"
        verbose_name_plural = "Listas de Exames"
        indexes = [models.Index(fields=['nome_lista'], name='lista_exames_idx')]

    def __str__(self):
        return self.nome_lista

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
        indexes = [models.Index(fields=['nome'], name='produto_nome_idx')]

    def __str__(self):
        return self.nome

    def clean(self):
        super().clean()
        if self.validade < timezone.now().date():
            raise ValidationError("A validade do produto não pode ser no passado.")
        if self.data_ultima_reposicao > timezone.now().date():
            raise ValidationError("A data da última reposição não pode ser no futuro.")

    def precisa_repor(self):
        return self.quantidade < self.quantidade_minima

class Estoque(models.Model):
    id_estoque = models.BigAutoField(primary_key=True)
    produtos = models.ManyToManyField(Produto, related_name="estoques")
    nome_estoque = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Estoque"
        verbose_name_plural = "Estoques"
        indexes = [models.Index(fields=['nome_estoque'], name='estoque_nome_idx')]

    def __str__(self):
        return self.nome_estoque

class Cirurgia(models.Model):
    id_cirurgia = models.BigAutoField(primary_key=True)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    especie = models.ForeignKey(Especie, on_delete=models.CASCADE)
    raca = models.ForeignKey(Raca, on_delete=models.CASCADE)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    tipo_cirurgia = models.CharField(max_length=100)
    veterinario = models.CharField(max_length=100)
    responsavel = models.CharField(max_length=100)
    data_cirurgia = models.DateField()
    observacoes = models.TextField(blank=True, null=True)
    pos_cirurgicas = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Cirurgia"
        verbose_name_plural = "Cirurgias"
        indexes = [models.Index(fields=['animal', 'data_cirurgia'], name='cirurgia_idx')]

    def __str__(self):
        return f"{self.animal.nome} - {self.tipo_cirurgia}"

    def clean(self):
        super().clean()
        if self.data_cirurgia > timezone.now().date():
            raise ValidationError("A data da cirurgia não pode ser no futuro.")
        if self.tutor != self.animal.tutor and self.animal.tutor is not None:
            raise ValidationError("O tutor da cirurgia deve ser o mesmo do animal.")
        if self.especie != self.animal.especie or self.raca != self.animal.raca:
            raise ValidationError("Espécie e raça devem corresponder ao animal.")

class Internacao(models.Model):
    id_internacao = models.BigAutoField(primary_key=True)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    especie = models.ForeignKey(Especie, on_delete=models.CASCADE)
    raca = models.ForeignKey(Raca, on_delete=models.CASCADE)
    motivo_internacao = models.TextField()
    data_entrada = models.DateField()
    data_saida = models.DateField(blank=True, null=True)
    status_recuperacao = models.CharField(max_length=50)
    observacoes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Internação"
        verbose_name_plural = "Internações"
        indexes = [models.Index(fields=['animal', 'data_entrada'], name='internacao_idx')]

    def __str__(self):
        return f"{self.animal.nome} - {self.motivo_internacao}"

    def clean(self):
        super().clean()
        if self.data_entrada > timezone.now().date():
            raise ValidationError("A data de entrada não pode ser no futuro.")
        if self.data_saida and self.data_saida < self.data_entrada:
            raise ValidationError("A data de saída não pode ser anterior à data de entrada.")
        if self.especie != self.animal.especie or self.raca != self.animal.raca:
            raise ValidationError("Espécie e raça devem corresponder ao animal.")

class ConsultaClinica(models.Model):
    id_consulta = models.BigAutoField(primary_key=True)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='consultas')
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    motivo_atendimento = models.TextField()
    valor_consulta = models.DecimalField(max_digits=10, decimal_places=2)
    valor_medicamentos = models.DecimalField(max_digits=10, decimal_places=2)
    resultado = models.TextField(blank=True)
    observacoes = models.TextField(blank=True, null=True)
    data_hora = models.DateTimeField(
        verbose_name="Data e Hora da Consulta",
        default=timezone.now
    )

    class Meta:
        verbose_name = "Consulta Clínica"
        verbose_name_plural = "Consultas Clínicas"
        indexes = [models.Index(fields=['animal', 'data_hora'], name='consulta_idx')]

    def __str__(self):
        return f"Consulta {self.id_consulta} - {self.animal.nome}"

    def clean(self):
        super().clean()
        if self.valor_consulta < 0 or self.valor_medicamentos < 0:
            raise ValidationError("Os valores não podem ser negativos.")
        if self.data_hora > timezone.now():
            raise ValidationError("A data e hora da consulta não podem ser no futuro.")
        if self.tutor != self.animal.tutor and self.animal.tutor is not None:
            raise ValidationError("O tutor da consulta deve ser o mesmo do animal.")

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
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    especie = models.ForeignKey(Especie, on_delete=models.CASCADE)
    raca = models.ForeignKey(Raca, on_delete=models.CASCADE)
    idade = models.IntegerField()
    sexo = models.CharField(max_length=10, choices=[('M', 'Macho'), ('F', 'Fêmea')])
    peso = models.FloatField()
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    telefone_contato = models.CharField(max_length=15)
    procedimento = models.TextField()
    medicamentos = models.TextField()
    dosagem = models.CharField(max_length=50)
    frequencia = models.CharField(max_length=50)
    orientacoes_tutor = models.TextField()
    data_retorno = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = "Relatório de Atendimento"
        verbose_name_plural = "Relatórios de Atendimento"
        indexes = [models.Index(fields=['animal', 'data_atendimento'], name='relatorio_atendimento_idx')]

    def __str__(self):
        return f"Relatório {self.id_relatorio} - {self.animal.nome}"

    def clean(self):
        super().clean()
        if self.data_atendimento > timezone.now().date():
            raise ValidationError("A data de atendimento não pode ser no futuro.")
        if self.data_retorno and self.data_retorno < self.data_atendimento:
            raise ValidationError("A data de retorno não pode ser anterior à data de atendimento.")
        if self.tutor != self.animal.tutor and self.animal.tutor is not None:
            raise ValidationError("O tutor do relatório deve ser o mesmo do animal.")
        if self.especie != self.animal.especie or self.raca != self.animal.raca:
            raise ValidationError("Espécie e raça devem corresponder ao animal.")

class RelatorioAcompanhamento(models.Model):
    id_acompanhamento = models.BigAutoField(primary_key=True)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    especie = models.ForeignKey(Especie, on_delete=models.CASCADE)
    raca = models.ForeignKey(Raca, on_delete=models.CASCADE)
    idade = models.IntegerField()
    sexo = models.CharField(max_length=10, choices=[('M', 'Macho'), ('F', 'Fêmea')])
    peso = models.FloatField()
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    telefone = models.CharField(max_length=15)
    endereco = models.TextField()
    email = models.EmailField(max_length=60)
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
        indexes = [models.Index(fields=['animal', 'data_atendimento'], name='relatorio_acompanhamento_idx')]

    def __str__():
        return f"Acompanhamento {self.id_acompanhamento} - {self.animal.nome}"

    def clean(self):
        super().clean()
        if self.data_atendimento > timezone.now().date():
            raise ValidationError("A data de atendimento não pode ser no futuro.")
        if self.data_aplicacao_exame > timezone.now().date():
            raise ValidationError("A data de aplicação/exame não pode ser no futuro.")
        if self.data_prevista_proximo and self.data_prevista_proximo < self.data_aplicacao_exame:
            raise ValidationError("A data prevista para o próximo evento não pode ser anterior à data de aplicação/exame.")
        if self.tutor != self.animal.tutor and self.animal.tutor is not None:
            raise ValidationError("O tutor do acompanhamento deve ser o mesmo do animal.")
        if self.especie != self.animal.especie or self.raca != self.animal.raca:
            raise ValidationError("Espécie e raça devem corresponder ao animal.")