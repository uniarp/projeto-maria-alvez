from django.contrib import admin
from gestao.models import (
    Tutor, Especie, Raca, Animal, Vacina, Medicamento, Exame, Prestadores,
    VacinaVermifugos, AnimalCastracao, ListaCastracao, ExameVeterinario,
    ListaExames, Produto, Estoque, Cirurgia, Internacao, ConsultaClinica,
    RelatorioAtendimento, RelatorioAcompanhamento
)

@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    list_display = ['cpf', 'nome', 'sobrenome', 'nome_completo', 'data_nascimento']
    list_filter = ['data_nascimento']
    search_fields = ['cpf', 'nome', 'sobrenome']
    readonly_fields = ['nome_completo']
    fieldsets = (
        (None, {
            'fields': ('cpf', 'nome', 'sobrenome', 'data_nascimento')
        }),
        ('Contato', {
            'fields': ('email', 'telefone', 'cep', 'endereco')
        }),
        ('Informações Calculadas', {
            'fields': ('nome_completo',)
        }),
    )

@admin.register(Especie)
class EspecieAdmin(admin.ModelAdmin):
    list_display = ['nome']
    search_fields = ['nome']

@admin.register(Raca)
class RacaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'especie']
    list_filter = ['especie']
    search_fields = ['nome']

@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ['nome', 'tutor', 'especie', 'raca', 'idade', 'data_cadastro']
    list_filter = ['especie', 'raca', 'data_cadastro']
    search_fields = ['nome', 'tutor__nome', 'tutor__sobrenome']

@admin.register(Vacina)
class VacinaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'especie', 'validade']
    list_filter = ['especie', 'validade']
    search_fields = ['nome']

@admin.register(Medicamento)
class MedicamentoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'estoque', 'validade']
    list_filter = ['validade']
    search_fields = ['nome']

@admin.register(Exame)
class ExameAdmin(admin.ModelAdmin):
    list_display = ['nome', 'tipo', 'especie']
    list_filter = ['tipo', 'especie']
    search_fields = ['nome']

@admin.register(Prestadores)
class PrestadoresAdmin(admin.ModelAdmin):
    list_display = ['nome']
    search_fields = ['nome']

@admin.register(VacinaVermifugos)
class VacinaVermifugosAdmin(admin.ModelAdmin):
    list_display = ['animal', 'tipo', 'data_aplicacao']
    list_filter = ['data_aplicacao']
    search_fields = ['animal__nome', 'tipo']

@admin.register(AnimalCastracao)
class AnimalCastracaoAdmin(admin.ModelAdmin):
    list_display = ['animal', 'status_castracao', 'data_cadastro']
    list_filter = ['status_castracao', 'data_cadastro']
    search_fields = ['animal__nome']

@admin.register(ListaCastracao)
class ListaCastracaoAdmin(admin.ModelAdmin):
    list_display = ['nome_lista']
    search_fields = ['nome_lista']

@admin.register(ExameVeterinario)
class ExameVeterinarioAdmin(admin.ModelAdmin):
    list_display = ['animal', 'tipo_exame', 'data_exame']
    list_filter = ['data_exame']
    search_fields = ['animal__nome', 'tipo_exame']

@admin.register(ListaExames)
class ListaExamesAdmin(admin.ModelAdmin):
    list_display = ['nome_lista']
    search_fields = ['nome_lista']

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'quantidade', 'validade']
    list_filter = ['validade']
    search_fields = ['nome']

@admin.register(Estoque)
class EstoqueAdmin(admin.ModelAdmin):
    list_display = ['nome_estoque']
    search_fields = ['nome_estoque']

@admin.register(Cirurgia)
class CirurgiaAdmin(admin.ModelAdmin):
    list_display = ['animal', 'tipo_cirurgia', 'data_cirurgia']
    list_filter = ['data_cirurgia']
    search_fields = ['animal__nome', 'tipo_cirurgia']

@admin.register(Internacao)
class InternacaoAdmin(admin.ModelAdmin):
    list_display = ['animal', 'motivo_internacao', 'data_entrada']
    list_filter = ['data_entrada']
    search_fields = ['animal__nome', 'motivo_internacao']

@admin.register(ConsultaClinica)
class ConsultaClinicaAdmin(admin.ModelAdmin):
    list_display = ['tutor', 'motivo_atendimento', 'data_hora']
    list_filter = ['data_hora']
    search_fields = ['tutor__nome', 'motivo_atendimento']

@admin.register(RelatorioAtendimento)
class RelatorioAtendimentoAdmin(admin.ModelAdmin):
    list_display = ['animal', 'tipo_atendimento', 'data_atendimento']
    list_filter = ['data_atendimento', 'tipo_atendimento']
    search_fields = ['animal__nome', 'tipo_atendimento']

@admin.register(RelatorioAcompanhamento)
class RelatorioAcompanhamentoAdmin(admin.ModelAdmin):
    list_display = ['animal', 'tipo_atendimento', 'data_atendimento']
    list_filter = ['data_atendimento', 'tipo_atendimento']
    search_fields = ['animal__nome', 'tipo_atendimento']