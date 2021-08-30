from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} company'

class SiteEr(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username