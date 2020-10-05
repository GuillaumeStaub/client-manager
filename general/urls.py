from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('commandes/',views.CommandesViewList.as_view(), name='commandes'),
    path('commande/<int:pk>',views.CommandeDetailView.as_view(), name='comande_detail'),
    path('create/client', views.CreateClientView.as_view(), name='create_client'),
    path('delete/<int:pk>', views.ClientDelete.as_view(), name='delete'),
    path('update/<int:pk>', views.UpdateClientView.as_view(), name='update_client'),
    path('ajax_forfait/', views.ajax_forfait, name='ajax_forfait'),
    path('ajax_search/client/', views.clients_search_view, name='ajax_search_client'),
    path('ajax_payee/', views.ajax_payee,name='ajax_payee'),
    path('ajax_ach/', views.ajax_ach,name='ajax_ach'),
    path('commande/pdf/<int:pk>', views.CommandePDFView.as_view(), name='commande_pdf'),
]
