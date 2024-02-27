from django.db import models
from django.contrib.auth.models import User

class Expense(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    amount = models.FloatField()
    CATEGORY_CHOICES = [
        ('Jedzenie', 'Jedzenie'),
        ('Rozrywka', 'Rozrywka'),
        ('Zakupy', 'Zakupy'),
        ('Rachunki', 'Rachunki'),
    ]
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    date = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.name