from dealer.models import Materials
from django.shortcuts import redirect
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import  UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views.generic import FormView
from .forms import AddMaterialsForm

class MaterialCreateView(UserPassesTestMixin, SuccessMessageMixin, FormView):
    template_name = 'dealer/materials_form.html'
    form_class = AddMaterialsForm
    success_url = '/dealer/addMaterials'
    success_message = "%(item)s was created successfully"
    
    def get_initial(self):
        return { 'dealer':self.request.user }
    
    def form_valid(self, form):
        form.instance.dealer = self.request.user.dealer
        form.save()
        return super().form_valid(form)

    def test_func(self):
        return hasattr(self.request.user, 'dealer')

    def handle_no_permission(self):
        messages.info(self.request, 'Login with your dealer id to view dealer specific pages')
        return redirect('/login')




class DealerDashboardView(UserPassesTestMixin, TemplateView):
    template_name = 'dealer/dealer_dashboard.html'

    def test_func(self):
        return hasattr(self.request.user, 'dealer')
    
    def handle_no_permission(self):
        messages.info(self.request, 'Login with your dealer id to view dealer specific pages')
        return redirect('/login')

class MaterialListView(UserPassesTestMixin, ListView):
    model = Materials
    context_object_name = 'material_list'

    def test_func(self):
        return hasattr(self.request.user, 'dealer')
    
    def handle_no_permission(self):
        messages.info(self.request, 'Login with your dealer id to view dealer specific pages')
        return redirect('/login')
