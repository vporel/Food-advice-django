from django.contrib import admin

from app.models import Aliment, AlimentRecette, Contributeur, OrigineRepas, Recette, Repas, Restaurant, TypeAliment
# Register your models here.

admin.site.register(Repas)
admin.site.register(OrigineRepas)
admin.site.register(Contributeur)
admin.site.register(Restaurant)
admin.site.register(Recette)
admin.site.register(Aliment)
admin.site.register(TypeAliment)
admin.site.register(AlimentRecette)