from django.shortcuts import redirect
from django.views.generic import TemplateView, ListView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from .models import BillItem, Project
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import user_passes_test, login_required



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
    fields = ['name', 'address', 'site_er']

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
    



class ProjectMaterialRequestView(UserPassesTestMixin, SuccessMessageMixin, CreateView):
    template_name = 'company/material_request.html'
    success_message = '%(item_name)s was created successfully'
    model = BillItem
    fields = ['item_name', 'quantity', 'unit']

    def get_success_url(self) -> str:
        pk = self.kwargs['pk']
        return f'/company/siteEr/request/{pk}/'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        project = Project.objects.get(id=self.kwargs['pk'])
        billitems = project.billitem_set.filter(state='E')
        if billitems.count() > 0:
            context['enable'] = billitems.count()
        context['bill_items'] = billitems
        return context

    def form_valid(self, form):
        project = Project.objects.get(id=self.kwargs['pk'])
        form.instance.siteer = self.request.user.siteer
        form.instance.project = project
        return super().form_valid(form)

    def test_func(self):
        return hasattr(self.request.user, 'siteer')

    def handle_no_permission(self):
        messages.info(self.request, 'Login with your company id to view company specific pages')
        return redirect('/login')


def siteEr_test_func(user):
    return hasattr(user, 'siteer')


@login_required(login_url='/login')
@user_passes_test(siteEr_test_func, login_url='/login')
def projectMaterialsDeleteView(request, item_id):
    item = BillItem.objects.get(pk=item_id)
    pk = item.project.pk
    messages.add_message(request, messages.WARNING, f'{item.item_name} is deleted')
    item.delete()
    return redirect(f'/company/siteEr/request/{pk}/')



class PastMaterialRequestListView(UserPassesTestMixin, TemplateView):
    template_name = 'company/past_request_list.html'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        project = Project.objects.get(pk=self.kwargs['project_id'])
        context['bill_items'] = project.billitem_set.exclude(state='E')
        return context

    def test_func(self):
        return hasattr(self.request.user, 'siteer')

    def handle_no_permission(self):
        messages.info(self.request, 'Login with your company id to view company specific pages')
        return redirect('/login')


class RequestSuccess(UserPassesTestMixin, TemplateView):
    template_name = 'company/material_request_complete.html'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        project = Project.objects.get(pk=self.kwargs['project_id'])
        billitems = project.billitem_set.filter(state='E')
        for billitem in billitems:
            billitem.state = 'P'
            billitem.save()
            project.pending_request += 1
        project.save()
        context['bill_items'] = billitems
        return context

    def test_func(self):
        return hasattr(self.request.user, 'siteer')

    def handle_no_permission(self):
        messages.info(self.request, 'Login with your company id to view company specific pages')
        return redirect('/login')



class ProjectsOrderView(UserPassesTestMixin, TemplateView):
    template_name = 'company/order_project_view.html'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['project_list'] = Project.objects.exclude(pending_request = 0).order_by('pending_request')
        return context

    def test_func(self):
        return hasattr(self.request.user, 'company')

    def handle_no_permission(self):
        messages.info(self.request, 'Login with your company id to view company specific pages')
        return redirect('/login')

class ProjectOrderListView(UserPassesTestMixin, SuccessMessageMixin, CreateView):
    template_name = 'company/project_order_list.html'
    model = BillItem
    fields = ['item_name', 'quantity', 'unit', 'site_er']
    success_message = '%(item_name)s was created successfully'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['bill_items_pending'] = Project.objects.get(pk=self.kwargs['project_id']).billitem_set.filter(state='P')
        context['bill_items_ordered'] = Project.objects.get(pk=self.kwargs['project_id']).billitem_set.filter(state='O')
        context['bill_items_accepted'] = Project.objects.get(pk=self.kwargs['project_id']).billitem_set.filter(state='A')
        context['bill_items_delivered'] = Project.objects.get(pk=self.kwargs['project_id']).billitem_set.filter(state='D')
        return context

    def test_func(self):
        return hasattr(self.request.user, 'company')

    def handle_no_permission(self):
        messages.info(self.request, 'Login with your company id to view company specific pages')
        return redirect('/login')

    def form_valid(self, form):
        project = Project.objects.get(id=self.kwargs['project_id'])
        form.instance.project = project
        form.instance.state = 'P'
        project.pending_request += 1
        project.save()
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs['project_id']
        return f'/company/order/{pk}/'


def company_test_func(user):
    return hasattr(user, 'company')

@login_required(login_url='/login')
@user_passes_test(company_test_func, login_url='/login')
def placedRequestRejectView(request, item_id):
    item = BillItem.objects.get(pk=item_id)
    pk = item.project.pk
    project = Project.objects.get(pk=pk)
    project.pending_request -= 1
    project.save()
    messages.add_message(request, messages.WARNING, f'{item.item_name} is rejected')
    item.state = 'R'
    item.save()
    return redirect(f'/company/order/{pk}/')

class OrderPastRequestListView(UserPassesTestMixin, SuccessMessageMixin, TemplateView):
    template_name = 'company/order_past_request.html'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        project = Project.objects.get(pk=self.kwargs['project_id'])
        context['bill_items'] = project.billitem_set.filter(state='D')
        return context

    def test_func(self):
        return hasattr(self.request.user, 'company')

    def handle_no_permission(self):
        messages.info(self.request, 'Login with your company id to view company specific pages')
        return redirect('/login')