from rest_framework import serializers
from .models import Medicamento,Animal, FotoAnimal, Adocao,CadastroAnimalAdocao

class MedicamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicamento
        fields = ['id', 'nome', 'quantidade', 'validade']

class FotoAnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = FotoAnimal
        fields = '__all__'

class CadastroAnimalAdocaoSerializer(serializers.ModelSerializer):
    fotos = FotoAnimalSerializer(many=True, read_only=True)

    class Meta:
        model = CadastroAnimalAdocao
        fields = '__all__'

class AdocaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adocao
        fields = '__all__'
