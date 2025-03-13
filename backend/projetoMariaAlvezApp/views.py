# backend/projetoMariaAlvezApp/views.py
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Medicamento

def sample_api(request):
    return Response({"message": "Exemplo de API funcionando!"})

class MedicamentoListCreateView(APIView):
    def get(self, request):
        medicamentos = Medicamento.objects.all()
        return Response({"medicamentos": [m.nome for m in medicamentos]})

    def post(self, request):
        nome = request.data.get('nome', 'Novo Medicamento')
        medicamento = Medicamento.objects.create(nome=nome)
        return Response({"status": "Medicamento criado", "id": medicamento.id})

class MedicamentoRemoveView(APIView):
    def delete(self, request, pk=None):
        if pk:
            try:
                medicamento = Medicamento.objects.get(id=pk)
                medicamento.delete()
                return Response({"status": "Medicamento removido"})
            except Medicamento.DoesNotExist:
                return Response({"error": "Medicamento não encontrado"}, status=404)
        return Response({"error": "ID do medicamento é necessário"}, status=400)