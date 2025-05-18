from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Tutor, Animal, RelatorioAtendimento, FilaCastracao, CandidatoAdocao, Funcionario
from .serializers import (
    TutorSerializer, AnimalSerializer, RelatorioAtendimentoSerializer,
    FilaCastracaoSerializer, CandidatoAdocaoSerializer, FuncionarioSerializer
)

class TutorViewSet(viewsets.ModelViewSet):
    queryset = Tutor.objects.all()
    serializer_class = TutorSerializer
    permission_classes = [IsAuthenticated]  # Apenas usuários autenticados
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['cadastro_unico', 'estado']  # Filtros exatos
    search_fields = ['nome', 'sobrenome', 'cpf']  # Campos para busca textual
    ordering_fields = ['nome', 'data_cadastro']  # Campos para ordenação
    ordering = ['nome']  # Ordenação padrão

    def get_queryset(self):
        # Otimiza consultas evitando múltiplos acessos ao banco
        return Tutor.objects.select_related().all()

class AnimalViewSet(viewsets.ModelViewSet):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['especie', 'raca', 'castrado', 'disponivel_adocao']
    search_fields = ['nome']
    ordering_fields = ['nome', 'data_cadastro', 'idade']
    ordering = ['nome']

    def get_queryset(self):
        # Otimiza consultas para ForeignKeys (tutor, especie, raca)
        return Animal.objects.select_related('tutor', 'especie', 'raca').all()

class RelatorioAtendimentoViewSet(viewsets.ModelViewSet):
    queryset = RelatorioAtendimento.objects.all()
    serializer_class = RelatorioAtendimentoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['animal', 'tutor', 'tipo_atendimento']
    search_fields = ['animal__nome', 'vet_responsavel', 'diagnostico_inicial']
    ordering_fields = ['data_atendimento', 'animal__nome']
    ordering = ['-data_atendimento']  # Mais recentes primeiro

    def get_queryset(self):
        # Otimiza consultas para ForeignKeys
        return RelatorioAtendimento.objects.select_related('animal', 'tutor', 'especie', 'raca').all()

    def perform_create(self, serializer):
        # Garante que o tutor do relatório corresponde ao tutor do animal
        instance = serializer.save()
        if instance.tutor != instance.animal.tutor:
            raise serializers.ValidationError("O tutor do relatório deve ser o mesmo do animal.")

class FilaCastracaoViewSet(viewsets.ModelViewSet):
    queryset = FilaCastracao.objects.all()
    serializer_class = FilaCastracaoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'animal']
    search_fields = ['animal__nome']
    ordering_fields = ['posicao', 'data_cadastro', 'data_prevista_castracao']
    ordering = ['posicao']

    def get_queryset(self):
        # Otimiza consultas para ForeignKey (animal)
        return FilaCastracao.objects.select_related('animal').all()

    def perform_create(self, serializer):
        # Verifica se o animal já está na fila com status 'AGUARDANDO'
        animal = serializer.validated_data['animal']
        if FilaCastracao.objects.filter(animal=animal, status='AGUARDANDO').exists():
            raise serializers.ValidationError("Este animal já está na fila de castração.")
        serializer.save()

class CandidatoAdocaoViewSet(viewsets.ModelViewSet):
    queryset = CandidatoAdocao.objects.all()
    serializer_class = CandidatoAdocaoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'animal', 'tutor']
    search_fields = ['tutor__nome', 'animal__nome']
    ordering_fields = ['data_candidatura', 'tutor__nome']
    ordering = ['-data_candidatura']  # Mais recentes primeiro

    def get_queryset(self):
        # Otimiza consultas para ForeignKeys
        return CandidatoAdocao.objects.select_related('tutor', 'animal').all()

    def perform_create(self, serializer):
        # Verifica se o animal está disponível para adoção
        animal = serializer.validated_data['animal']
        if not animal.disponivel_adocao:
            raise serializers.ValidationError("Este animal não está disponível para adoção.")
        serializer.save()

class FuncionarioViewSet(viewsets.ModelViewSet):
    queryset = Funcionario.objects.all()
    serializer_class = FuncionarioSerializer
    permission_classes = [IsAdminUser]  # Apenas superusuários
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['cargo']
    search_fields = ['nome', 'cpf']
    ordering_fields = ['nome']
    ordering = ['nome']

    def get_queryset(self):
        # Otimiza consultas para ForeignKey (usuario)
        return Funcionario.objects.select_related('usuario').all()