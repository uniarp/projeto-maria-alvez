from rest_framework import serializers
from .models import Tutor, Animal, RelatorioAtendimento, FilaCastracao, CandidatoAdocao, Funcionario

class TutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = ['id', 'nome', 'cpf', 'rg', 'endereco', 'email', 'telefone', 'cadastro_unico']

class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = ['id', 'nome', 'raca', 'cor', 'sexo', 'deficiencia', 'tutor', 'castrado', 'disponivel_adocao']

class RelatorioAtendimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelatorioAtendimento
        fields = ['id', 'animal', 'tutor', 'data_atendimento', 'diagnostico_inicial', 'procedimento', 'observacoes']

class FilaCastracaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilaCastracao
        fields = ['id', 'animal', 'posicao', 'status']

class CandidatoAdocaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidatoAdocao
        fields = ['id', 'tutor', 'animal', 'data_candidatura', 'status']

class FuncionarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funcionario
        fields = ['id', 'usuario', 'nome', 'cpf', 'rg', 'endereco', 'email', 'telefone', 'cargo']