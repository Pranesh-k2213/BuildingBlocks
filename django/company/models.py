from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} company'



class SiteEr(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username



class Project(models.Model):
    name = models.CharField(max_length=50)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    site_er = models.ForeignKey(SiteEr, on_delete=models.SET_NULL, null = True)
    address = models.TextField(max_length=250)
    is_completed = models.BooleanField(default=False)


    def __str__(self):
        return f'{self.name} project'
