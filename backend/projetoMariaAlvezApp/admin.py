from django.contrib import admin
from .models import (
    Tutor, Especie, Raca, Animal, Vacina, Medicamento, Exame,
)

# Registre as classes no painel de administração
admin.site.register(Tutor)
admin.site.register(Especie)
admin.site.register(Raca)
admin.site.register(Animal)
admin.site.register(Vacina)
admin.site.register(Medicamento)
admin.site.register(Exame)