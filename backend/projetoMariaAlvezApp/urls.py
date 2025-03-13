from django.urls import path
from .views import sample_api, MedicamentoListCreateView, MedicamentoRemoveView

urlpatterns = [
    path('sample/', sample_api, name='sample'),  # Para /api/sample/
    path('medicamentos/', MedicamentoListCreateView.as_view(), name='medicamento-list-create'),
    path('medicamentos/remover/', MedicamentoRemoveView.as_view(), name='medicamento-remove'),
]