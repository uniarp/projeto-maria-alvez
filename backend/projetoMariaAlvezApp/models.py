from validate_docbr import CPF
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from datetime import timedelta

class Tutor(models.Model):
    id_tutor = models.BigAutoField(primary_key=True, verbose_name="ID do Tutor")
    nome = models.CharField(max_length=80, verbose_name="Nome")
    sobrenome = models.CharField(max_length=80, verbose_name="Sobrenome")
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
    'Digite um CEP válido no formato: 12345-678, 12345678, ou 12345 678.'
)]
    )
    email = models.EmailField(verbose_name="E-mail")
    telefone = models.CharField(
        max_length=15,
        verbose_name="Telefone",
        validators=[RegexValidator(
    r'^\+?55?\s?(\(?\d{2}\)?\s?)?\d{8,9}|\d{10,11}$',
    'Digite um número de telefone válido no formato: +55 (DD) XXXX-XXXX, (DD) XXXX-XXXX'
)]
    )
    cpf = models.CharField(
    max_length=14,
    verbose_name="CPF",
    unique=True,
    validators=[RegexValidator(
    r'^\d{3}\.?\d{3}\.?\d{3}-?\d{2}$|\d{11}$',
    'Digite um CPF válido no formato: 123.456.789-00 ou 01234567890 (11 dígitos). O CPF será armazenado como 01234567890 (somente dígitos).'
)]
)

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
        """Retorna uma representação legível do tutor no formato 'Nome Sobrenome - CPF'."""
        return f"{self.nome} {self.sobrenome} - {self.cpf}"

    def clean(self):
        """Valida o CPF antes de salvar."""
        super().clean()
        cpf_validator = CPF()
        if not cpf_validator.validate(self.cpf.replace('.', '').replace('-', '')):
            raise ValidationError("O CPF informado é inválido.")

    @property
    def nome_completo(self):
        """Retorna o nome completo do tutor."""
        return f"{self.nome} {self.sobrenome}"

class Especie(models.Model):
    id_especie = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=80)

    class Meta:
        verbose_name = "Espécie"
        verbose_name_plural = "Espécies"

    def __str__(self):
        return self.nome

class Raca(models.Model):
    id_raca = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=80)
    especie = models.ForeignKey(Especie, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Raça"
        verbose_name_plural = "Raças"

    def __str__(self):
        return self.nome

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
        validators=[MinValueValidator(0, "A idade deve ser maior ou igual a 0")],
    )
    especie = models.ForeignKey(Especie, on_delete=models.CASCADE, verbose_name="Espécie", related_name="animais")
    data_cadastro = models.DateField(
        verbose_name="Data de Cadastro",
        default=timezone.now,
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
        """Valida a idade e a consistência dos relacionamentos."""
        super().clean()
        if self.idade < 0:
            raise ValidationError("A idade do animal não pode ser negativa.")
        if not self.tutor:
            raise ValidationError("Um animal deve ter um tutor associado.")
        if not self.raca or not self.especie:
            raise ValidationError("Raça e espécie são obrigatórios.")
        if self.data_cadastro > timezone.now().date():
            raise ValidationError("A data de cadastro não pode ser no futuro.")

    @property
    def idade_em_meses(self):
        """Calcula a idade do animal em meses."""
        from datetime import date
        hoje = date.today()
        meses = (hoje.year - self.data_cadastro.year) * 12 + (hoje.month - self.data_cadastro.month)
        return max(0, meses)  # Garante que não seja negativo

    def eh_valido(self):
        """Verifica se o animal tem idade válida e tutor associado."""
        return self.idade >= 0 and self.tutor is not None

    def get_absolute_url(self):
        """Retorna a URL para visualizar o animal no admin ou API."""
        from django.urls import reverse
        return reverse('animal-detail', kwargs={'pk': self.pk})  # Ajuste o nome da URL conforme necessário

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

    class Meta:
        verbose_name = "Vacina"
        verbose_name_plural = "Vacinas"

    def __str__(self):
        return self.nome

class Medicamento(models.Model):
    id_medicamento = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    quantidade = models.IntegerField()
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
    estoque = models.IntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    validade = models.DateField()
    data_registro = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Medicamento"
        verbose_name_plural = "Medicamentos"

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
    especie = models.ForeignKey(Especie, on_delete=models.CASCADE)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    equipamento = models.CharField(max_length=100, blank=True, null=True)
    duracao = models.DurationField(help_text="Duração média do exame (hh:mm:ss)")
    recomendacoes_pre = models.TextField(blank=True, null=True)
    data_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Exame"
        verbose_name_plural = "Exames"

    def __str__(self):
        return self.nome

class Prestadores(models.Model):
    id_prestador = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Prestador"
        verbose_name_plural = "Prestadores"

    def __str__(self):
        return self.nome

class VacinaVermifugos(models.Model):
    id_vacina_vermifugo = models.BigAutoField(primary_key=True)
    nome_animal = models.CharField(max_length=80)
    especie = models.ForeignKey(Especie, on_delete=models.CASCADE)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50)
    data_aplicacao = models.DateField()
    data_proximo_reforco = models.DateField(blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Vacina/Vermífugo"
        verbose_name_plural = "Vacinas/Vermífugos"

    def __str__(self):
        return f"{self.nome_animal} - {self.tipo}"

    def calcular_proximo_reforco(self):
        if self.data_aplicacao:
            self.data_proximo_reforco = self.data_aplicacao + timedelta(days=30)
            self.save()

class AnimalCastracao(models.Model):
    id_castracao = models.BigAutoField(primary_key=True)
    nome_animal = models.CharField(max_length=80)
    posicao_fila = models.IntegerField()
    especie = models.ForeignKey(Especie, on_delete=models.CASCADE)
    raca = models.ForeignKey(Raca, on_delete=models.CASCADE)
    sexo = models.CharField(max_length=10, choices=[('M', 'Macho'), ('F', 'Fêmea')])
    idade = models.IntegerField()
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    data_cadastro = models.DateField()
    status_castracao = models.CharField(max_length=20, choices=[('Pendente', 'Pendente'), ('Realizada', 'Realizada')])
    data_prevista_castracao = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = "Animal para Castração"
        verbose_name_plural = "Animais para Castração"

    def clean(self):
        super().clean()
        if self.data_prevista_castracao and self.data_cadastro:
            if self.data_prevista_castracao < self.data_cadastro:
                raise ValidationError("A data prevista para castração não pode ser anterior à data de cadastro.")

    def __str__(self):
        return f"{self.nome_animal} - {self.status_castracao}"

class ListaCastracao(models.Model):
    id_lista = models.BigAutoField(primary_key=True)
    animais = models.ManyToManyField(AnimalCastracao)
    nome_lista = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Lista de Castração"
        verbose_name_plural = "Listas de Castração"

    def __str__(self):
        return self.nome_lista

class ExameVeterinario(models.Model):
    id_exame_vet = models.BigAutoField(primary_key=True)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
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

class ListaExames(models.Model):
    id_lista_exames = models.BigAutoField(primary_key=True)
    exames = models.ManyToManyField(ExameVeterinario)
    nome_lista = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Lista de Exames"
        verbose_name_plural = "Listas de Exames"

    def __str__(self):
        return self.nome_lista

class Produto(models.Model):
    id_produto = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    quantidade = models.IntegerField()
    validade = models.DateField()
    fornecedor = models.CharField(max_length=100)
    quantidade_minima = models.IntegerField()
    data_ultima_reposicao = models.DateField()

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"

    def __str__(self):
        return self.nome

    def precisa_repor(self):
        return self.quantidade < self.quantidade_minima

class Estoque(models.Model):
    id_estoque = models.BigAutoField(primary_key=True)
    produtos = models.ManyToManyField(Produto)
    nome_estoque = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Estoque"
        verbose_name_plural = "Estoques"

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

    def __str__(self):
        return f"{self.animal.nome} - {self.tipo_cirurgia}"

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

    def __str__(self):
        return f"{self.animal.nome} - {self.motivo_internacao}"

class ConsultaClinica(models.Model):
    id_consulta = models.BigAutoField(primary_key=True)
    motivo_atendimento = models.TextField()
    valor_consulta = models.DecimalField(max_digits=10, decimal_places=2)
    valor_medicamentos = models.DecimalField(max_digits=10, decimal_places=2)
    observacoes = models.TextField(blank=True, null=True)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    data_hora = models.DateTimeField(
        verbose_name="Data e Hora da Consulta",
        default=timezone.now
    )

    class Meta:
        verbose_name = "Consulta Clínica"
        verbose_name_plural = "Consultas Clínicas"

    def __str__(self):
        return f"Consulta {self.id_consulta} - {self.tutor}"

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

    def __str__(self):
        return f"Relatório {self.id_relatorio} - {self.animal.nome}"

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

    def __str__(self):
        return f"Acompanhamento {self.id_acompanhamento} - {self.animal.nome}"