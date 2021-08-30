from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
     path('', views.CompanyDashboardView.as_view(), name='company-dashboard'),
]