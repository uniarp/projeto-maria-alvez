from django.contrib import admin
from .models import (
    Tutor, Especie, Raca, Animal, Vacina, Medicamento, Exame, Prestadores,
    VacinaVermifugos, AnimalCastracao, ListaCastracao, ExameVeterinario,
    ListaExames, Produto, Estoque, Cirurgia, Internacao, ConsultaClinica,
    RelatorioAtendimento, RelatorioAcompanhamento,CadastroAnimalAdocao, FotoAnimal, Adocao
)

@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sobrenome', 'cpf', 'email', 'telefone')
    search_fields = ('nome', 'sobrenome', 'cpf', 'email')
    list_filter = ('estado', 'cidade')

@admin.register(Especie)
class EspecieAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(Raca)
class RacaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'especie')
    search_fields = ('nome',)
    list_filter = ('especie',)

@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tutor', 'raca', 'especie', 'idade')
    search_fields = ('nome', 'tutor__nome', 'tutor__sobrenome')
    list_filter = ('especie', 'raca')

@admin.register(Vacina)
class VacinaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'especie', 'dose', 'validade', 'custo')
    search_fields = ('nome', 'fabricante')
    list_filter = ('especie', 'validade')

@admin.register(Medicamento)
class MedicamentoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'principio_ativo', 'administracao', 'estoque', 'preco', 'validade')
    search_fields = ('nome', 'principio_ativo', 'fabricante')
    list_filter = ('administracao', 'validade')

@admin.register(Exame)
class ExameAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'especie', 'preco', 'data_registro')
    search_fields = ('nome',)
    list_filter = ('tipo', 'especie')

@admin.register(Prestadores)
class PrestadoresAdmin(admin.ModelAdmin):
    list_display = ('nome',)

@admin.register(VacinaVermifugos)
class VacinaVermifugosAdmin(admin.ModelAdmin):
    list_display = ('nome_animal', 'especie', 'tutor', 'tipo', 'data_aplicacao', 'data_proximo_reforco')
    search_fields = ('nome_animal', 'tutor__nome', 'tutor__sobrenome')
    list_filter = ('especie', 'tipo', 'data_aplicacao')

@admin.register(AnimalCastracao)
class AnimalCastracaoAdmin(admin.ModelAdmin):
    list_display = ('nome_animal', 'posicao_fila', 'especie', 'raca', 'sexo', 'status_castracao', 'data_prevista_castracao')
    search_fields = ('nome_animal', 'tutor__nome', 'tutor__sobrenome')
    list_filter = ('especie', 'raca', 'sexo', 'status_castracao')

@admin.register(ListaCastracao)
class ListaCastracaoAdmin(admin.ModelAdmin):
    list_display = ('nome_lista',)
    filter_horizontal = ('animais',)

@admin.register(ExameVeterinario)
class ExameVeterinarioAdmin(admin.ModelAdmin):
    list_display = ('animal', 'tutor', 'tipo_exame', 'data_exame', 'veterinario_solicitante')
    search_fields = ('animal__nome', 'tutor__nome', 'tutor__sobrenome', 'veterinario_solicitante')
    list_filter = ('tipo_exame', 'data_exame')

@admin.register(ListaExames)
class ListaExamesAdmin(admin.ModelAdmin):
    list_display = ('nome_lista',)
    filter_horizontal = ('exames',)

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'quantidade', 'validade', 'fornecedor', 'quantidade_minima')
    search_fields = ('nome', 'fornecedor')
    list_filter = ('validade',)

@admin.register(Estoque)
class EstoqueAdmin(admin.ModelAdmin):
    list_display = ('nome_estoque',)
    filter_horizontal = ('produtos',)

@admin.register(Cirurgia)
class CirurgiaAdmin(admin.ModelAdmin):
    list_display = ('animal', 'tipo_cirurgia', 'veterinario', 'data_cirurgia')
    search_fields = ('animal__nome', 'veterinario', 'responsavel')
    list_filter = ('tipo_cirurgia', 'data_cirurgia')

@admin.register(Internacao)
class InternacaoAdmin(admin.ModelAdmin):
    list_display = ('animal', 'motivo_internacao', 'data_entrada', 'data_saida', 'status_recuperacao')
    search_fields = ('animal__nome',)
    list_filter = ('status_recuperacao', 'data_entrada')

@admin.register(ConsultaClinica)
class ConsultaClinicaAdmin(admin.ModelAdmin):
    list_display = ('id_consulta', 'motivo_atendimento', 'tutor', 'data_hora', 'valor_consulta', 'valor_medicamentos')
    search_fields = ('motivo_atendimento', 'tutor__nome', 'tutor__sobrenome')
    list_filter = ('data_hora',)

    def get_total(self, obj):
        return obj.calcular_total()
    get_total.short_description = 'Total'

@admin.register(RelatorioAtendimento)
class RelatorioAtendimentoAdmin(admin.ModelAdmin):
    list_display = ('id_relatorio', 'animal', 'data_atendimento', 'tipo_atendimento', 'vet_responsavel')
    search_fields = ('animal__nome', 'vet_responsavel', 'diagnostico_inicial')
    list_filter = ('tipo_atendimento', 'data_atendimento')

@admin.register(RelatorioAcompanhamento)
class RelatorioAcompanhamentoAdmin(admin.ModelAdmin):
    list_display = ('id_acompanhamento', 'animal', 'data_atendimento', 'tipo_atendimento', 'vet_responsavel')
    search_fields = ('animal__nome', 'vet_responsavel', 'diagnostico')
    list_filter = ('tipo_atendimento', 'data_atendimento', 'tipo_vacina_exame')
    
class FotoInline(admin.TabularInline):
    model = FotoAnimal
    extra = 1

@admin.register(CadastroAnimalAdocao) 
class CadastroAnimalAdocaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'especie', 'raca', 'idade', 'sexo', 'tamanho', 'peso', 'adotado')
    search_fields = ('nome', 'especie', 'raca')
    list_filter = ('especie', 'sexo', 'tamanho', 'adotado')
    inlines = [FotoInline]

@admin.register(Adocao)
class AdocaoAdmin(admin.ModelAdmin):
    list_display = ('animal', 'nome_adotante', 'cpf_cnpj', 'data_adocao')
    search_fields = ('nome_adotante', 'cpf_cnpj')


