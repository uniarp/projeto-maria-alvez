from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Medicamento
from .serializers import MedicamentoSerializer

class MedicamentoListCreateView(APIView):
    def get(self, request):
        medicamentos = Medicamento.objects.all()
        serializer = MedicamentoSerializer(medicamentos, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MedicamentoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MedicamentoRemoveView(APIView):
    def post(self, request):
        nome = request.data.get('nome')
        quantidade = request.data.get('quantidade')
        try:
            medicamento = Medicamento.objects.get(nome=nome)
            if medicamento.quantidade >= quantidade:
                medicamento.quantidade -= quantidade
                medicamento.save()
                return Response({"message": f"{quantidade} unidades de {nome} removidas."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Quantidade insuficiente."}, status=status.HTTP_400_BAD_REQUEST)
        except Medicamento.DoesNotExist:
            return Response({"error": f"Medicamento {nome} não encontrado."}, status=status.HTTP_404_NOT_FOUND)
