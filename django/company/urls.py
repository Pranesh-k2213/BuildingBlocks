from django.urls import path
from . import views

urlpatterns = [
     path('', views.CompanyDashboardView.as_view(), name='company-dashboard'),
     path('project/', views.ProjectListView.as_view(), name='project-list'),
     path('project/create/', views.ProjectCreateView.as_view(), name='project-create'),
     path('project/<int:pk>/update/', views.ProjectUpdateView.as_view(), name='project-update'),
     path('project/<int:pk>/delete', views.ProjectDeleteView.as_view(), name='project-delete'),
]