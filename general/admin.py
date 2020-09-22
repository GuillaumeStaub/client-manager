from django.contrib import admin
from .models import Client, InfosTechniques, Saison, Forfait, Commande, Evenement


# Register your models here.
class CommandeInline(admin.TabularInline):
    list_display = ('infos_techniques',)
    model = Commande
    extra = 1


class ClientAdmin(admin.ModelAdmin):
    search_fields = ['nom', 'prenom', 'telephone', 'societe_manege']
    model = Client
    inlines = [CommandeInline, ]


# Register your models here.
admin.site.register(Client, ClientAdmin)
admin.site.register(InfosTechniques)
admin.site.register(Saison)
admin.site.register(Forfait)
admin.site.register(Commande)
admin.site.register(Evenement)
