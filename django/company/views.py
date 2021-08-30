from django.shortcuts import redirect
from django.views.generic import TemplateView, ListView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from .models import Project
from django.contrib.messages.views import SuccessMessageMixin



class CompanyDashboardView(UserPassesTestMixin, TemplateView):
    template_name = 'company/company_dashboard.html'

    def test_func(self):
        return hasattr(self.request.user, 'company')
    
    def handle_no_permission(self):
        messages.info(self.request, 'Login with your company id to view company specific pages')
        return redirect('/login')



class SiteErDashboardView(UserPassesTestMixin, TemplateView):
    template_name = 'company/siteer_dashboard.html'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['projects'] = self.request.user.siteer.project_set.all()
        return context

    def test_func(self):
        return hasattr(self.request.user, 'siteer')

    def handle_no_permission(self):
        messages.info(self.request, 'Login with your Site Engineer id to view requested pages')
        return redirect('/login')



class ProjectListView(UserPassesTestMixin, ListView):
    model = Project

    def test_func(self):
        return hasattr(self.request.user, 'company')

    def handle_no_permission(self):
        messages.info(self.request, 'Login with your company id to view company specific pages')
        return redirect('/login')


class ProjectCreateView(UserPassesTestMixin, SuccessMessageMixin, CreateView):
    template_name = 'company/project_create_form.html'
    success_url = '/company/project'
    success_message = '%(name)s was created successfully'
    model = Project
    fields = fields = ['name', 'address', 'site_er']

    def form_valid(self, form):
        form.instance.company = self.request.user.company
        form.save()
        return super().form_valid(form)

    
    def test_func(self):
        return hasattr(self.request.user, 'company')

    def handle_no_permission(self):
        messages.info(self.request, 'Login with your company id to view company specific pages')
        return redirect('/login')


class ProjectUpdateView(UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Project
    fields = ['name', 'site_er', 'is_completed', 'address']
    success_url = '/company/project'
    success_message = '%(name)s was edited successfully'
    template_name = 'company/project_update_form.html'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        project = self.get_object()
        context['id'] = project.pk
        return context

    def form_valid(self, form):
        form.instance.company = self.request.user.company
        return super().form_valid(form)

    def test_func(self):
        project = self.get_object()
        if project.company == self.request.user.company and hasattr(self.request.user, 'company'):
            return True
        return False

    def handle_no_permission(self):
        messages.info(self.request, 'Login with your company id to view company specific pages')
        return redirect('/login')


class ProjectDeleteView(UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    template_name = 'company/project_confirm_delete.html'
    model = Project
    success_url = '/company/project'
    success_message = '%(name)s was edited successfully'

    def test_func(self):
        project = self.get_object()
        if project.company == self.request.user.company and hasattr(self.request.user, 'company'):
            return True
        return False

    def handle_no_permission(self):
        messages.info(self.request, 'Login with your company id to view company specific pages')
        return redirect('/login')
    