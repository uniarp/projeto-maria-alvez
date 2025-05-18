from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from gestao.views import TutorViewSet, AnimalViewSet, RelatorioAtendimentoViewSet, ListaCastracaoViewSet

router = DefaultRouter()
router.register(r'tutores', TutorViewSet)
router.register(r'animais', AnimalViewSet)
router.register(r'relatorios-atendimento', RelatorioAtendimentoViewSet)
router.register(r'listas-castracao', ListaCastracaoViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', include('gestao.urls')),
]