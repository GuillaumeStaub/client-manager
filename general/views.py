from django.shortcuts import render
from .models import Client, Commande
from django.db.models import Sum
from django.views.generic import ListView


class HomeView(ListView):
    model = Client
    context_object_name = "clients"
    template_name = "general/home.html"
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nb_clients'] = Client.objects.count()
        context['total_commandes'] = round(Commande.objects.filter(payee=True).aggregate(Sum('total_ttc'))['total_ttc__sum'],2)
        context['nb_commandes'] = Commande.objects.count()
        context['field_names'] = ['Nom', 'Prenom', 'Téléphone', 'Ville']
        return context
