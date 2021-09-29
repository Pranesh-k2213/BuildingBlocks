from django.contrib import admin
from .models import Company, SiteEr, Project, BillItem

# Register your models here.
admin.site.register(Company)
admin.site.register(SiteEr)
admin.site.register(Project)
admin.site.register(BillItem)