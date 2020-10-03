from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('create/client', views.CreateClientView.as_view(), name='create_client'),
    path('delete/<int:pk>', views.ClientDelete.as_view(), name='delete'),
    path('update/<int:pk>', views.UpdateClientView.as_view(), name='update_client'),
    path('ajax_forfait/',views.ajax_forfait, name='ajax_forfait'),
]
