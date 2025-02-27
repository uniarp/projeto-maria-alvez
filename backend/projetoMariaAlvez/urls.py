from django.contrib import admin
from django.urls import path
from projetoMariaAlvezApp.views import MedicamentoListCreateView, MedicamentoRemoveView
from .views import sample_api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/sample/', sample_api),  # Aqui você chama a view 'sample_api' do seu projeto
    path('api/medicamentos/', MedicamentoListCreateView.as_view(), name='medicamento-list-create'),
    path('api/medicamentos/remover/', MedicamentoRemoveView.as_view(), name='medicamento-remove'),
]
