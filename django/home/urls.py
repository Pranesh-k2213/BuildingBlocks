from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='home/about.html'), name='about'),
    path('login/', views.loginView, name='login'),
    path('success/', TemplateView.as_view(template_name='home/success.html'), name='success'),
    path('logout/', views.logoutView, name='logout'),
]