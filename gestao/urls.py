from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TutorViewSet, AnimalViewSet, EspecieViewSet, RacaViewSet, VacinaViewSet,
    MedicamentoViewSet, ExameViewSet, VacinaVermifugosViewSet, AnimalCastracaoViewSet,
    ListaCastracaoViewSet, ExameVeterinarioViewSet, ListaExamesViewSet, EstoqueViewSet,
    CirurgiaViewSet, InternacaoViewSet, ConsultaClinicaViewSet, RelatorioAtendimentoViewSet,
    RelatorioAcompanhamentoViewSet, PrestadoresViewSet, ProdutoViewSet
)

router = DefaultRouter()
router.register(r'tutores', TutorViewSet)
router.register(r'animais', AnimalViewSet)
router.register(r'especies', EspecieViewSet)
router.register(r'racas', RacaViewSet)
router.register(r'vacinas', VacinaViewSet)
router.register(r'medicamentos', MedicamentoViewSet)
router.register(r'exames', ExameViewSet)
router.register(r'vacinas-vermifugos', VacinaVermifugosViewSet)
router.register(r'animais-castracao', AnimalCastracaoViewSet)
router.register(r'listas-castracao', ListaCastracaoViewSet)
router.register(r'exames-veterinarios', ExameVeterinarioViewSet)
router.register(r'listas-exames', ListaExamesViewSet)
router.register(r'estoque', EstoqueViewSet)
router.register(r'cirurgias', CirurgiaViewSet)
router.register(r'internacoes', InternacaoViewSet)
router.register(r'consultas-clinicas', ConsultaClinicaViewSet)
router.register(r'relatorios-atendimento', RelatorioAtendimentoViewSet)
router.register(r'relatorios-acompanhamento', RelatorioAcompanhamentoViewSet)
router.register(r'prestadores', PrestadoresViewSet)
router.register(r'produtos', ProdutoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]