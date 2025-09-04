from django.urls import path
from .views import sample_api, MedicamentoListCreateView, MedicamentoRemoveView, CadastroAnimalAdocaoViewSet, AdocaoViewSet
urlpatterns = [
        path('sample/', sample_api, name='sample'),  # Para /api/sample/
        path('medicamentos/', MedicamentoListCreateView.as_view(), name='medicamento-list-create'),
        path('medicamentos/remover/', MedicamentoRemoveView.as_view(), name='medicamento-remove'),
        # Endpoints para Animais
        path('animais/', CadastroAnimalAdocaoViewSet.as_view(), name='animal-list-create'),
        path('animais/<int:pk>/', CadastroAnimalAdocaoViewSet.as_view(), name='animal-detail'),

        # Endpoints para Adoções
        path('adocoes/', AdocaoViewSet.as_view(), name='adocao-list-create'),
        path('adocoes/<int:pk>/', AdocaoViewSet.as_view(), name='adocao-detail'),
    ]