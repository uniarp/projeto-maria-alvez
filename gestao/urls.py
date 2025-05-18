from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TutorViewSet, AnimalViewSet, RelatorioAtendimentoViewSet,
    FilaCastracaoViewSet, CandidatoAdocaoViewSet, FuncionarioViewSet
)

router = DefaultRouter()
router.register(r'tutores', TutorViewSet)
router.register(r'animais', AnimalViewSet)
router.register(r'atendimentos', RelatorioAtendimentoViewSet)
router.register(r'fila-castracao', FilaCastracaoViewSet)
router.register(r'candidatos-adocao', CandidatoAdocaoViewSet)
router.register(r'funcionarios', FuncionarioViewSet)

urlpatterns = [
    path('', include(router.urls)),
]