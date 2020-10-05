from django.shortcuts import render
from django.conf import settings
from .forms import ClientForm
from .models import Client, Commande, Forfait
from django.db.models import Q
from django.db.models import Sum
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSetFactory
from easy_pdf.views import PDFTemplateResponseMixin
from datetime import datetime


class HomeView(LoginRequiredMixin, ListView):
    """
    This view shows the list of customers by adding in the context additional information such as the number of
    Vorders, or the sum of orders paid.
    """
    model = Client
    context_object_name = "clients"
    template_name = "general/home.html"
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nb_clients'] = Client.objects.count()
        context['total_commandes'] = Commande.objects.filter(payee=True).aggregate(Sum('total_ttc'))['total_ttc__sum']
        context['nb_commandes'] = Commande.objects.count()
        context['field_names'] = ['Nom', 'Prenom', 'Téléphone', 'Commune']
        return context


class CommandeInline(InlineFormSetFactory):
    """
    This class adds a formset to my CreateClientiew to add orders to my new client.
    """
    model = Commande
    fields = '__all__'
    factory_kwargs = {'extra': 2, 'can_order': False, 'can_delete': False}


class CreateClientView(LoginRequiredMixin, CreateWithInlinesView):
    """
    This generic view allows you to create a new customer and add new orders to it.
    """
    model = Client
    fields = '__all__'
    inlines = [CommandeInline, ]
    template_name = 'general/create_client.html'
    success_url = reverse_lazy('home')


class ClientDelete(LoginRequiredMixin, DeleteView):
    """
    This generic view allows you to delete a customer and his orders
    """
    model = Client
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class UpdateClientView(LoginRequiredMixin, UpdateWithInlinesView):
    """
    This generic view allows you to update a customer and his orders and create new command for customer
    """
    model = Client
    form_class = ClientForm
    inlines = [CommandeInline, ]
    template_name = 'general/update_client.html'
    success_url = reverse_lazy('home')


@login_required
def ajax_forfait(request):
    if request.method == 'GET':
        if request.GET['forfait_name']:
            forfait_name = request.GET['forfait_name']
            forfait = Forfait.objects.get(nom=forfait_name)
            forfait_price_ht = forfait.prix_ht
            forfait_price_ttc = forfait.prix_ttc
            forfait_taxe = forfait.taxe
            response = JsonResponse({"forfait_price_ht": forfait_price_ht, "forfait_price_ttc": forfait_price_ttc,
                                     "forfait_taxe": forfait_taxe})
            response.status_code = 200  # To announce that the user isn't allowed to publish
            return response
        else:
            forfait_price_ht = 0.00
            forfait_price_ttc = 0.00
            forfait_taxe = 20.00
            response = JsonResponse({"forfait_price_ht": forfait_price_ht, "forfait_price_ttc": forfait_price_ttc,
                                     "forfait_taxe": forfait_taxe})
            response.status_code = 200  # To announce that the user isn't allowed to publish
            return response


@login_required
def clients_search_view(request):
    url_parameter = request.GET.get("q")
    if url_parameter:
        clients = Client.objects.filter(Q(nom__icontains=url_parameter) | Q(telephone__icontains=url_parameter))
    else:
        clients = Client.objects.all()
    field_names = ['Nom', 'Prenom', 'Téléphone', 'Ville']
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string(
            template_name="general/table_clients.html",
            context={"clients": clients, "field_names": field_names}
        )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)

    return render(request, "general/home.html", context={"clients": clients, "field_names": field_names})


class CommandePDFView(LoginRequiredMixin, PDFTemplateResponseMixin, DetailView):
    model = Commande
    base_url = 'file://{}/'.format(settings.STATIC_ROOT)
    template_name = 'general/PDF.html'

    def get_context_data(self, **kwargs):
        context = super(CommandePDFView, self).get_context_data(**kwargs)
        context['TVA_calc'] = round(context['commande'].forfait.prix_ht * (context['commande'].forfait.taxe / 100), 2) * \
                              context['commande'].nb_jours
        context['date'] = datetime.now()
        return context


class CommandesView(LoginRequiredMixin, ListView):
    model = Commande
    context_object_name = "commandes"
    template_name = "general/commandes_list.html"
    paginate_by = 50
    ordering = ['-date_commande']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nb_commandes'] = Commande.objects.count()
        context['total_commandes_payee'] = Commande.objects.filter(payee=True).aggregate(Sum('total_ttc'))[
            'total_ttc__sum']
        context['total_commandes_non_payee'] = Commande.objects.filter(payee=False).aggregate(Sum('total_ttc'))[
            'total_ttc__sum']
        context['field_names'] = ['Evènement', 'Saison', 'Client', 'Payée', 'Traitée par ACH', 'Date']
        return context
