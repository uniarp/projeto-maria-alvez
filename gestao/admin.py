from django.contrib import admin
from .models import Tutor, Animal, Funcionario, RelatorioAtendimento, FilaCastracao, CandidatoAdocao

admin.site.register(Tutor)
admin.site.register(Animal)
admin.site.register(Funcionario)
admin.site.register(RelatorioAtendimento)
admin.site.register(FilaCastracao)
admin.site.register(CandidatoAdocao)