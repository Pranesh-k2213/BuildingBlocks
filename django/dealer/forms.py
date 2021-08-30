from django import forms
from .models import Materials

class AddMaterialsForm(forms.ModelForm):
    class Meta:
        model = Materials
        fields = ['item', 'unit']