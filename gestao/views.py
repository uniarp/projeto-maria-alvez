from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import (
    Tutor, Animal, Especie, Raca, Vacina, Medicamento, Exame, VacinaVermifugos,
    AnimalCastracao, ListaCastracao, ExameVeterinario, ListaExames, Estoque,
    Cirurgia, Internacao, ConsultaClinica, RelatorioAtendimento, RelatorioAcompanhamento,
    Prestadores, Produto
)
from .serializers import (
    TutorSerializer, AnimalSerializer, EspecieSerializer, RacaSerializer, VacinaSerializer,
    MedicamentoSerializer, ExameSerializer, VacinaVermifugosSerializer, AnimalCastracaoSerializer,
    ListaCastracaoSerializer, ExameVeterinarioSerializer, ListaExamesSerializer, EstoqueSerializer,
    CirurgiaSerializer, InternacaoSerializer, ConsultaClinicaSerializer, RelatorioAtendimentoSerializer,
    RelatorioAcompanhamentoSerializer, PrestadoresSerializer, ProdutoSerializer
)

class TutorViewSet(viewsets.ModelViewSet):
    queryset = Tutor.objects.all()
    serializer_class = TutorSerializer

class AnimalViewSet(viewsets.ModelViewSet):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer

class EspecieViewSet(viewsets.ModelViewSet):
    queryset = Especie.objects.all()
    serializer_class = EspecieSerializer

class RacaViewSet(viewsets.ModelViewSet):
    queryset = Raca.objects.all()
    serializer_class = RacaSerializer

class VacinaViewSet(viewsets.ModelViewSet):
    queryset = Vacina.objects.all()
    serializer_class = VacinaSerializer

class MedicamentoViewSet(viewsets.ModelViewSet):
    queryset = Medicamento.objects.all()
    serializer_class = MedicamentoSerializer

class ExameViewSet(viewsets.ModelViewSet):
    queryset = Exame.objects.all()
    serializer_class = ExameSerializer

class VacinaVermifugosViewSet(viewsets.ModelViewSet):
    queryset = VacinaVermifugos.objects.all()
    serializer_class = VacinaVermifugosSerializer

class AnimalCastracaoViewSet(viewsets.ModelViewSet):
    queryset = AnimalCastracao.objects.all()
    serializer_class = AnimalCastracaoSerializer

class ListaCastracaoViewSet(viewsets.ModelViewSet):
    queryset = ListaCastracao.objects.all()
    serializer_class = ListaCastracaoSerializer

class ExameVeterinarioViewSet(viewsets.ModelViewSet):
    queryset = ExameVeterinario.objects.all()
    serializer_class = ExameVeterinarioSerializer

class ListaExamesViewSet(viewsets.ModelViewSet):
    queryset = ListaExames.objects.all()
    serializer_class = ListaExamesSerializer

class EstoqueViewSet(viewsets.ModelViewSet):
    queryset = Estoque.objects.all()
    serializer_class = EstoqueSerializer

class CirurgiaViewSet(viewsets.ModelViewSet):
    queryset = Cirurgia.objects.all()
    serializer_class = CirurgiaSerializer

class InternacaoViewSet(viewsets.ModelViewSet):
    queryset = Internacao.objects.all()
    serializer_class = InternacaoSerializer

class ConsultaClinicaViewSet(viewsets.ModelViewSet):
    queryset = ConsultaClinica.objects.all()
    serializer_class = ConsultaClinicaSerializer

class RelatorioAtendimentoViewSet(viewsets.ModelViewSet):
    queryset = RelatorioAtendimento.objects.all()
    serializer_class = RelatorioAtendimentoSerializer

class RelatorioAcompanhamentoViewSet(viewsets.ModelViewSet):
    queryset = RelatorioAcompanhamento.objects.all()
    serializer_class = RelatorioAcompanhamentoSerializer

class PrestadoresViewSet(viewsets.ModelViewSet):
    queryset = Prestadores.objects.all()
    serializer_class = PrestadoresSerializer

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer