from rest_framework import serializers
from .models import (
    Tutor, Animal, Especie, Raca, Vacina, Medicamento, Exame, VacinaVermifugos,
    AnimalCastracao, ListaCastracao, ExameVeterinario, ListaExames, Estoque,
    Cirurgia, Internacao, ConsultaClinica, RelatorioAtendimento, RelatorioAcompanhamento,
    Prestadores, Produto
)

class TutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = '__all__'

class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = '__all__'

class EspecieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especie
        fields = '__all__'

class RacaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Raca
        fields = '__all__'

class VacinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacina
        fields = '__all__'

class MedicamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicamento
        fields = '__all__'

class ExameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exame
        fields = '__all__'

class VacinaVermifugosSerializer(serializers.ModelSerializer):
    class Meta:
        model = VacinaVermifugos
        fields = '__all__'

class AnimalCastracaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalCastracao
        fields = '__all__'

class ListaCastracaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListaCastracao
        fields = '__all__'

class ExameVeterinarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExameVeterinario
        fields = '__all__'

class ListaExamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListaExames
        fields = '__all__'

class EstoqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estoque
        fields = '__all__'

class CirurgiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cirurgia
        fields = '__all__'

class InternacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Internacao
        fields = '__all__'

class ConsultaClinicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultaClinica
        fields = '__all__'

class RelatorioAtendimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelatorioAtendimento
        fields = '__all__'

class RelatorioAcompanhamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelatorioAcompanhamento
        fields = '__all__'

class PrestadoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prestadores
        fields = '__all__'

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = '__all__'