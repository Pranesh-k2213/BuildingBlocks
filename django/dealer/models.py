from django.db import models
from django.contrib.auth.models import User
from company.models import Company

# Create your models here.
class Dealer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ManyToManyField(Company, through='Ties')

    def __str__(self):
        return f'{self.user.username} dealer'

class Ties(models.Model):
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    formed_on = models.DateField()

    def __str__(self):
        return f'{self.dealer.user.username}-{self.company.user.username} tie'

class Materials(models.Model):
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE)
    item = models.CharField(max_length=50, unique=True)
    unit = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.item}-{self.dealer.user.username}'