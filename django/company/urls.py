from django.urls import path
from . import views

urlpatterns = [
     path('', views.CompanyDashboardView.as_view(), name='company-dashboard'),
     path('project/', views.ProjectListView.as_view(), name='project-list'),
     path('project/create/', views.ProjectCreateView.as_view(), name='project-create'),
     path('project/<int:pk>/update/', views.ProjectUpdateView.as_view(), name='project-update'),
     path('project/<int:pk>/delete/', views.ProjectDeleteView.as_view(), name='project-delete'),
     path('siteEr/', views.SiteErDashboardView.as_view(), name='siteer-dashboard'),
     path('siteEr/request/<int:pk>/', views.ProjectMaterialRequestView.as_view(), name='material-request'),
     path('siteEr/request/item_delete/<int:item_id>/', views.projectMaterialsDeleteView, name='material-delete'),
     path('siteEr/past_request/<int:project_id>/', views.PastMaterialRequestListView.as_view(), name='past-material-request'),
     path('siteEr/request_success/<int:project_id>', views.RequestSuccess.as_view(), name='material-request-success'),
     path('order/project/', views.ProjectsOrderView.as_view(), name='order-projects'),
     path('order/<int:project_id>/', views.ProjectOrderListView.as_view(), name='project-order-list'),
     path('order/reject/<int:item_id>/', views.placedRequestRejectView, name='reject-placed-request'),
     path('order/past_requests/<int:project_id>/', views.OrderPastRequestListView.as_view(), name='order-past-request'),
]