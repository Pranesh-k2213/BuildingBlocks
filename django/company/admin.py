from django.contrib import admin
from .models import Company, SiteEr, Project

# Register your models here.
admin.site.register(Company)
admin.site.register(SiteEr)
admin.site.register(Project)