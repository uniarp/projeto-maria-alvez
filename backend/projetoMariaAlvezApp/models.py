from validate_docbr import CPF
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

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
    default='Oral'  # Define um valor padrão para os registros existentes
)
    fabricante = models.CharField(max_length=100)
    estoque = models.IntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    validade = models.DateField()
    data_registro = models.DateTimeField(default=timezone.now)

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


from django.db import models
from datetime import datetime, timedelta

# Create your models here.

class vacinaVermifugos:
    def __init__(self, nome_animal, especie, nome_tutor, tipo, data_aplicacao, data_proximo_reforco, observacoes=""):
        self.nome_animal = nome_animal
        self.especie = especie
        self.nome_tutor = nome_tutor
        self.tipo = tipo
        self.data_aplicacao = data_aplicacao
        self.data_proximo_reforco = data_proximo_reforco
        self.observacoes = observacoes

    def calcular_proximo_reforco(self, intervalo_dias):
        if self.data_aplicacao:
            self.data_proximo_reforco = self.data_aplicacao + timedelta(days=intervalo_dias)
        else:
            print("Data de aplicação não definida!")

    def exibir_dados(self):
        print(f"Nome do Animal: {self.nome_animal}")
        print(f"Espécie: {self.especie}")
        print(f"Nome do Tutor: {self.nome_tutor}")
        print(f"Tipo: {self.tipo}")
        print(f"Data da Aplicação: {self.data_aplicacao.strftime('%d/%m/%Y') if self.data_aplicacao else 'N/A'}")
        print(f"Data do Próximo Reforço: {self.data_proximo_reforco.strftime('%d/%m/%Y') if self.calcular_proximo_reforco else 'N/A'}")
        print(f"Observações: {self.observacoes}")


class animalCastracao:
    def __init__(self, nome_animal, posicao_fila, especie, raca, sexo, idade, nome_tutor, data_cadastro, status_castracao, data_prevista_castracao):
        self.nome_animal = nome_animal
        self.posicao_fila = posicao_fila
        self.especie = especie
        self.raca = raca
        self.sexo = sexo
        self.idade = idade
        self.nome_tutor = nome_tutor
        self.data_cadastro = datetime.strptime(data_cadastro, '%d/%m/%Y') if data_cadastro else None
        self.status_castracao = status_castracao
        self.data_prevista_castracao = datetime.strptime(data_prevista_castracao, '%d/%m/%Y') if data_prevista_castracao else None

    def exibir_dados(self):
        print(f"Nome do Animal: {self.nome_animal}")
        print(f"Posição na Fila: {self.posicao_fila}")
        print(f"Espécie: {self.especie}")
        print(f"Raça: {self.raca}")
        print(f"Sexo: {self.sexo}")
        print(f"Idade: {self.idade}")
        print(f"Nome do Tutor: {self.nome_tutor}")
        print(f"Data de Cadastro: {self.data_cadastro.strftime('%d/%m/%Y') if self.data_cadastro else 'N/A'}")
        print(f"Status da Castração: {self.status_castracao}")
        print(f"Data Prevista para Castração: {self.data_prevista_castracao.strftime('%d/%m/%Y') if self.data_prevista_castracao else 'N/A'}")

    def atualizar_status(self, novo_status):
        self.status_castracao = novo_status
        print(f"Status atualizado para: {self.status_castracao}")

class listaCastracao:
    def __init__ (self):
        self.animais = []

    def adicionar_animal(self, animal):
        self.animais.append(animal)
        print(f"Animal {animal.nome_animal} adicionado a lista de castração")

    def exibir_lista(self):
        print("Lista de Castração")
        for animal in self.animais:
            animal.exibir_dados()
            print("-" * 30)

    def filtrar_status(self, status):
        print(f"Animais com status '{status}':")
        filtrados = [animal for animal in self.animais if animal.status_castracao == status]
        for animal in filtrados:
            animal.exibir_dados()
            print("-" * 30)

    def buscar_por_id(self, id_animal):
        for animal in self.animais:
            if animal.id_animal == id_animal:
                return animal
        print(f"Animal com ID {id_animal} não encontrado.")
        return None

class ExameVeterinario:
    def __init__(self, id_exame, nome_animal, nome_tutor, tipo_exame, data_exame, veterinario_solicitante, resultados=None, observacoes=None):
        self.id_exame = id_exame  # Identificador único do exame
        self.nome_animal = nome_animal
        self.nome_tutor = nome_tutor
        self.tipo_exame = tipo_exame
        self.data_exame = datetime.strptime(data_exame, '%d/%m/%Y') if data_exame else None
        self.veterinario_solicitante = veterinario_solicitante
        self.resultados = resultados
        self.observacoes = observacoes

    def exibir_dados(self):
        print(f"ID do Exame: {self.id_exame}")
        print(f"Nome do Animal: {self.nome_animal}")
        print(f"Nome do Tutor: {self.nome_tutor}")
        print(f"Tipo de Exame: {self.tipo_exame}")
        print(f"Data do Exame: {self.data_exame.strftime('%d/%m/%Y') if self.data_exame else 'N/A'}")
        print(f"Veterinário Solicitante: {self.veterinario_solicitante}")
        print(f"Resultados: {self.resultados if self.resultados else 'Aguardando'}")
        print(f"Observações: {self.observacoes if self.observacoes else 'Nenhuma'}")
        print("-" * 40)

    def atualizar_resultados(self, novo_resultado):
        self.resultados = novo_resultado
        print(f"Resultados atualizados para: {self.resultados}")

    def adicionar_observacao(self, nova_observacao):
        if self.observacoes:
            self.observacoes += f" | {nova_observacao}"
        else:
            self.observacoes = nova_observacao
        print("Observação adicionada com sucesso!")

class ListaExames:
    def __init__(self):
        self.exames = []

    def adicionar_exame(self, exame):
        self.exames.append(exame)
        print(f"Exame de {exame.nome_animal} cadastrado com sucesso!")

    def exibir_lista(self):
        print("\nLista de Exames:")
        for exame in self.exames:
            exame.exibir_dados()

    def buscar_por_id(self, id_exame):
        for exame in self.exames:
            if exame.id_exame == id_exame:
                return exame
        print(f"Exame com ID {id_exame} não encontrado.")
        return None

    def filtrar_por_tipo(self, tipo_exame):
        print(f"\nExames do tipo '{tipo_exame}':")
        filtrados = [exame for exame in self.exames if exame.tipo_exame == tipo_exame]
        for exame in filtrados:
            exame.exibir_dados()

class Produto:
    def __init__(self, id_produto, nome, quantidade, validade, fornecedor, quantidade_minima, data_ultima_reposicao):
        self.id_produto = id_produto  # Identificador único do produto
        self.nome = nome
        self.quantidade = quantidade
        self.validade = datetime.strptime(validade, "%d/%m/%Y") if validade else None
        self.fornecedor = fornecedor
        self.quantidade_minima = quantidade_minima
        self.data_ultima_reposicao = datetime.strptime(data_ultima_reposicao, "%d/%m/%Y") if data_ultima_reposicao else None

    def exibir_dados(self):
        print(f"ID do Produto: {self.id_produto}")
        print(f"Nome: {self.nome}")
        print(f"Quantidade em Estoque: {self.quantidade}")
        print(f"Validade: {self.validade.strftime('%d/%m/%Y') if self.validade else 'N/A'}")
        print(f"Fornecedor: {self.fornecedor}")
        print(f"Quantidade Mínima: {self.quantidade_minima}")
        print(f"Última Reposição: {self.data_ultima_reposicao.strftime('%d/%m/%Y') if self.data_ultima_reposicao else 'N/A'}")
        print("-" * 40)

    def precisa_repor(self):
        return self.quantidade < self.quantidade_minima

    def atualizar_estoque(self, nova_quantidade, data_reposicao):
        self.quantidade = nova_quantidade
        self.data_ultima_reposicao = datetime.strptime(data_reposicao, "%d/%m/%Y")
        print(f"Estoque atualizado! Nova quantidade: {self.quantidade}")

class Estoque:
    def __init__(self):
        self.produtos = []

    def adicionar_produto(self, produto):
        self.produtos.append(produto)
        print(f"Produto '{produto.nome}' cadastrado com sucesso!")

    def exibir_estoque(self):
        print("\nRelatório de Estoque:")
        for produto in self.produtos:
            produto.exibir_dados()

    def verificar_necessidade_reposicao(self):
        print("\nProdutos que precisam de reposição:")
        for produto in self.produtos:
            if produto.precisa_repor():
                print(f"- {produto.nome} (Quantidade: {produto.quantidade} | Mínimo: {produto.quantidade_minima})")
        print("-" * 40)

    def buscar_por_nome(self, nome):
        for produto in self.produtos:
            if produto.nome.lower() == nome.lower():
                return produto
        print(f"Produto '{nome}' não encontrado.")
        return None

class Cirurgia:
    def __init__(self, nome_animal, especie, raca, nome_tutor, tipo_cirurgia, veterinario, responsavel, data_cirurgia, observacoes, pos_cirurgicas):
        self.nome_animal = nome_animal
        self.especie = especie
        self.raca = raca
        self.nome_tutor = nome_tutor
        self.tipo_cirurgia = tipo_cirurgia
        self.veterinario = veterinario
        self.responsavel = responsavel
        self.data_cirurgia = data_cirurgia
        self.observacoes = observacoes
        self.pos_cirurgicas = pos_cirurgicas

    def exibir_dados(self):
        print(f"Nome do Animal: {self.nome_animal}")
        print(f"Espécie: {self.especie}")
        print(f"Raça: {self.raca}")
        print(f"Nome do Tutor: {self.nome_tutor}")
        print(f"Tipo de Cirurgia: {self.tipo_cirurgia}")
        print(f"Veterinário: {self.veterinario}")
        print(f"Responsável: {self.responsavel}")
        print(f"Data da Cirurgia: {self.data_cirurgia}")
        print(f"Observações: {self.observacoes}")
        print(f"Pós-Cirúrgicas: {self.pos_cirurgicas}")

class Internacao:
    def __init__(self, nome_animal, especie, raca, motivo_internacao, data_entrada, data_saida, status_recuperacao, observacoes):
        self.nome_animal = nome_animal
        self.especie = especie
        self.raca = raca
        self.motivo_internacao = motivo_internacao
        self.data_entrada = data_entrada
        self.data_saida = data_saida
        self.status_recuperacao = status_recuperacao
        self.observacoes = observacoes

    def exibir_dados(self):
        print(f"Nome do Animal: {self.nome_animal}")
        print(f"Espécie: {self.especie}")
        print(f"Raça: {self.raca}")
        print(f"Motivo da Internação: {self.motivo_internacao}")
        print(f"Data de Entrada: {self.data_entrada}")
        print(f"Data de Saída: {self.data_saida}")
        print(f"Status da Recuperação: {self.status_recuperacao}")
        print(f"Observações: {self.observacoes}")

class ConsultaClinica:
    def __init__(self, id_consulta, motivo_atendimento, valor_consulta, valor_medicamentos, observacoes, data_hora, tutor):
        self.id_consulta = id_consulta
        self.motivo_atendimento = motivo_atendimento
        self.valor_consulta = valor_consulta
        self.valor_medicamentos = valor_medicamentos
        self.observacoes = observacoes
        self.data_hora = data_hora
        self.tutor = tutor

    def calcular_total(self):
        return self.valor_consulta + self.valor_medicamentos

    def exibir_dados(self):
        print(f"ID da Consulta: {self.id_consulta}")
        print(f"Motivo do Atendimento: {self.motivo_atendimento}")
        print(f"Valor da Consulta: R$ {self.valor_consulta:.2f}")
        print(f"Valor dos Medicamentos: R$ {self.valor_medicamentos:.2f}")
        print(f"Valor Total: R$ {self.calcular_total():.2f}")
        print(f"Observações: {self.observacoes}")
        print(f"Data e Hora: {self.data_hora}")
        print(f"Tutor: {self.tutor}")

class RelatorioAtendimento:
    def __init__(self, data_atendimento, hora_atendimento, tipo_atendimento, vet_responsavel, diagnostico_inicial, observacoes, nome_animal, especie, raca, 
                idade, sexo, peso, nome_tutor, telefone_contato, procedimento, medicamentos, dosagem, frequencia, orientacoes_tutor, data_retorno):
        self.data_atendimento = data_atendimento
        self.hora_atendimento = hora_atendimento
        self.tipo_atendimento = tipo_atendimento
        self.vet_responsavel = vet_responsavel
        self.diagnostico_inicial = diagnostico_inicial
        self.observacoes = observacoes
        self.nome_animal = nome_animal
        self.especie = especie
        self.raca = raca
        self.idade = idade
        self.sexo = sexo
        self.peso = peso
        self.nome_tutor = nome_tutor
        self.telefone_contato = telefone_contato
        self.procedimento = procedimento
        self.medicamentos = medicamentos
        self.dosagem = dosagem
        self.frequencia = frequencia
        self.orientacoes_tutor = orientacoes_tutor
        self.data_retorno = data_retorno

    def exibir_dados(self):
        print(f"\nData: {self.data_atendimento} Hora: {self.hora_atendimento}")
        print(f"Tipo de Atendimento: {self.tipo_atendimento}")
        print(f"Veterinário Responsável: {self.vet_responsavel}")
        print(f"Diagnóstico Inicial: {self.diagnostico_inicial}")
        print(f"Observações: {self.observacoes}")
        print(f"\nAnimal: {self.nome_animal} | Espécie: {self.especie} | Raça: {self.raca} | Idade: {self.idade} | Sexo: {self.sexo} | Peso: {self.peso}kg")
        print(f"Tutor: {self.nome_tutor} | Contato: {self.telefone_contato}")
        print(f"\nProcedimento Realizado: {self.procedimento}")
        print(f"Medicamentos Prescritos: {self.medicamentos} | Dosagem: {self.dosagem} | Frequência: {self.frequencia}")
        print(f"Orientações para o Tutor: {self.orientacoes_tutor}")
        print(f"Data para Retorno: {self.data_retorno}\n")

class RelatorioAcompanhamento:
    def __init__(self, nome_animal, especie, raca, idade, sexo, peso, nome_tutor, telefone, endereco, email, data_atendimento, tipo_atendimento, vet_responsavel, 
                 diagnostico, observacoes, procedimento,medicamentos, dosagem, frequencia, orientacoes_tutor, data_retorno, tipo_vacina_exame,data_aplicacao_exame, 
                 data_prevista_proximo, resultados_exames):
        self.nome_animal = nome_animal
        self.especie = especie
        self.raca = raca
        self.idade = idade
        self.sexo = sexo
        self.peso = peso
        self.nome_tutor = nome_tutor
        self.telefone = telefone
        self.endereco = endereco
        self.email = email
        self.data_atendimento = data_atendimento
        self.tipo_atendimento = tipo_atendimento
        self.vet_responsavel = vet_responsavel
        self.diagnostico = diagnostico
        self.observacoes = observacoes
        self.procedimento = procedimento
        self.medicamentos = medicamentos
        self.dosagem = dosagem
        self.frequencia = frequencia
        self.orientacoes_tutor = orientacoes_tutor
        self.data_retorno = data_retorno
        self.tipo_vacina_exame = tipo_vacina_exame
        self.data_aplicacao_exame = data_aplicacao_exame
        self.data_prevista_proximo = data_prevista_proximo
        self.resultados_exames = resultados_exames

    def exibir_dados(self):
        print("\n=== Relatório de Acompanhamento ===")
        print(f"Animal: {self.nome_animal} | Espécie: {self.especie} | Raça: {self.raca} | Idade: {self.idade} | Sexo: {self.sexo} | Peso: {self.peso}kg")
        print(f"Tutor: {self.nome_tutor} | Contato: {self.telefone} | Endereço: {self.endereco} | E-mail: {self.email}")
        print(f"\nData do Atendimento: {self.data_atendimento} | Tipo: {self.tipo_atendimento} | Veterinário: {self.vet_responsavel}")
        print(f"Diagnóstico: {self.diagnostico}")
        print(f"Observações: {self.observacoes}")
        print(f"\nProcedimento Realizado: {self.procedimento}")
        print(f"Medicamentos Prescritos: {self.medicamentos} | Dosagem: {self.dosagem} | Frequência: {self.frequencia}")
        print(f"Orientações para o Tutor: {self.orientacoes_tutor}")
        print(f"Data para Retorno: {self.data_retorno}")
        print(f"\nVacina/Exame: {self.tipo_vacina_exame}")
        print(f"Data da Aplicação/Exame: {self.data_aplicacao_exame} | Próxima: {self.data_prevista_proximo}")
        print(f"Resultados de Exames: {self.resultados_exames}\n")

class Consulta(models.Model):
    id_consulta = models.BigAutoField(primary_key=True)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    veterinario = models.CharField(max_length=100, help_text="Nome do veterinário responsável")  # Pode ser ajustado para um modelo de Veterinário no futuro
    data_consulta = models.DateTimeField(default=timezone.now, help_text="Data e hora da consulta")
    
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
    medicamentos_prescritos = models.ManyToManyField(Medicamento, blank=True, help_text="Medicamentos prescritos")
    exames_solicitados = models.ManyToManyField(Exame, blank=True, help_text="Exames solicitados")

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

    def _str_(self):
        return f"Consulta de {self.animal.nome} em {self.data_consulta.strftime('%d/%m/%Y %H:%M')}"