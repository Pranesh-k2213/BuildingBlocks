from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages



class CompanyDashboardView(UserPassesTestMixin, TemplateView):
    template_name = 'company/company_dashboard.html'

    def test_func(self):
        return hasattr(self.request.user, 'company')
    
    def handle_no_permission(self):
        messages.info(self.request, 'Login with your company id to view company specific pages')
        return redirect('/login')
