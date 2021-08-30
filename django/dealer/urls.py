from django.urls import path
from . import views

urlpatterns = [
    path('', views.DealerDashboardView.as_view(), name='dealer-dashboard'),
    path('addMaterials/', views.MaterialCreateView.as_view(), name='add-materials'),
    path('materialList', views.MaterialListView.as_view(), name='material-list'),
]