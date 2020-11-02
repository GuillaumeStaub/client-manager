from django.shortcuts import render
from django.conf import settings
import json
from .forms import ClientForm, CommandeForm
from .models import Client, Commande, Forfait
from django.db.models import Q
from django.db.models import Sum
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, UpdateView, CreateView
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
        context['total_commandes_non_payee'] = Commande.objects.filter(payee=False).aggregate(Sum('total_ttc'))[
            'total_ttc__sum']
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
    """
    This view allows you to send the customer via Ajax all the information about the selected package.
    The information is returned to the JSONResponse format, if the data is not found or blank a dictionary
    with zero values is returned.
    """
    if request.method == 'GET':
        if request.GET['forfait_name']:
            forfait_name = request.GET['forfait_name']
            forfait = Forfait.objects.get(nom=forfait_name)
            forfait_price_ht = forfait.prix_ht
            forfait_price_ttc = forfait.prix_ttc
            forfait_taxe = forfait.taxe
            forfait_description = forfait.description
            response = JsonResponse({"forfait_price_ht": forfait_price_ht, "forfait_price_ttc": forfait_price_ttc,
                                     "forfait_taxe": forfait_taxe, "forfait_description": forfait_description})
            response.status_code = 200  # To announce that the user isn't allowed to publish
            return response
        else:
            response = JsonResponse({"forfait_price_ht": 0.00, "forfait_price_ttc": 0.00,
                                     "forfait_taxe": 20.00, "forfait_description": ""})
            response.status_code = 200  # To announce that the user isn't allowed to publish
            return response


@login_required
def clients_search_view(request):
    """
    A view that allows you to return the search result to the customer via Ajax. Indeed, the filter is made on the
    customer's name and/or phone number. The search result is integrated into the client table and the html template
    returned to the client. The customer via JQuery replaces the old painting with the new one. If nothing is found
    or the search is empty the full template is returned.
    """
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


@login_required
def commande_search_view(request):
    """
        A view that allows you to return the search result to the Client via Ajax. Indeed, the filter is made on the
        customer's name and/or phone number. The search result is integrated into the client table and the html template
        returned to the client. The client via JQuery replaces the old painting with the new one. If nothing is found
        or the search is empty the full template is returned.
        """
    url_parameter = request.GET.get("q")
    if url_parameter:
        commandes = Commande.objects.filter(
            Q(client__nom__icontains=url_parameter) | Q(client__prenom__icontains=url_parameter))
    else:
        commandes = Commande.objects.all()
    field_names = ['Evènement', 'Saison', 'Client', 'Payée', 'Traitée par ACH', 'Date']
    if request.is_ajax():
        html = render_to_string(
            template_name="general/table_commandes.html",
            context={"commandes": commandes, "field_names": field_names}
        )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)

    return render(request, "general/commandes_list.html", context={"commandes": commandes, "field_names": field_names})


class CommandePDFView(LoginRequiredMixin, PDFTemplateResponseMixin, DetailView):
    """
    This view generates a summary of an order for a PDF customer.
    """
    model = Commande
    base_url = 'file://{}/'.format(settings.STATIC_ROOT)
    template_name = 'general/PDF.html'

    def get_context_data(self, **kwargs):
        context = super(CommandePDFView, self).get_context_data(**kwargs)
        context['TVA_calc'] = round(context['commande'].forfait.prix_ht * (context['commande'].forfait.taxe / 100), 2) * \
                              context['commande'].nb_jours
        context['date'] = datetime.now()
        return context


class CommandesViewList(LoginRequiredMixin, ListView):
    """
    This view lists the list of orders are added to the context the number of orders paid and unpaid, the number of orders
    """
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


class CommandeDetailView(LoginRequiredMixin, DetailView):
    """
    View that shows the detail of an order
    """
    model = Commande
    template_name = 'general/commande_detail.html'


@login_required
def ajax_payee(request):
    """
    This view makes it possible to make an order paid or not via the Detail view of the order and Ajax
    """
    if request.method == 'GET':
        if request.GET['payee'] and request.GET['id_commande']:
            Commande.objects.filter(pk=request.GET['id_commande']).update(payee=json.loads(request.GET['payee']))
            response = JsonResponse({})
            response.status_code = 200  # To announce that the user isn't allowed to publish
            return response
    response = JsonResponse({'payee': request.GET['payee']})
    response.status_code = 400  # To announce that the user isn't allowed to publish
    return response


@login_required
def ajax_ach(request):
    """
    This view makes it possible to make an order processed or not via the Detail view of the command and Ajax
    """
    if request.method == 'GET':
        print(json.loads(request.GET['traitee']))
        if request.GET['traitee'] and request.GET['id_commande']:
            Commande.objects.filter(pk=request.GET['id_commande']).update(traite_ach=json.loads(request.GET['traitee']))
            response = JsonResponse({})
            response.status_code = 200  # To announce that the user isn't allowed to publish
            return response
    response = JsonResponse({'traitee': request.GET['payee']})
    response.status_code = 400  # To announce that the user isn't allowed to publish
    return response


class CommandeCreateView(LoginRequiredMixin, CreateView):
    """
    View that allows you to create an order
    """
    model = Commande
    template_name = 'general/commande_create.html'
    form_class = CommandeForm
    success_url = reverse_lazy('commandes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date'] = datetime.now()
        return context


class CommandeUpdateView(LoginRequiredMixin, UpdateView):
    """
    View that allows you to update an order
    """
    model = Commande
    template_name = 'general/commande_update.html'
    form_class = CommandeForm
    success_url = reverse_lazy('commandes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date'] = Commande.objects.get(id=self.kwargs['pk']).date_commande
        return context


@login_required
def ajax_infos_client(request):
    """
    This view allows The Update and Create Order views by selecting a customer to retrieve their information with
    Ajax as his address, email ...
    """
    if request.method == 'GET':
        if request.GET['id']:
            id_client = request.GET['id']
            client = Client.objects.get(id=id_client)
            response = JsonResponse({"nom": client.nom, "prenom": client.prenom, "manege": client.societe_manege,
                                     "telephone": client.telephone, 'email': client.email,
                                     'adresse': f'{client.adresse} {client.code_postal} {client.commune}'})
            response.status_code = 200  # To announce that the user isn't allowed to publish
            return response
        else:
            response = JsonResponse({"prenom": ' ', "manege": ' ',
                                     "telephone": ' ', 'email': ' ',
                                     'adresse': ' '})
            response.status_code = 200  # To announce that the user isn't allowed to publish
            return response


def statistics_view(requests):
    pass
