
from django import forms
from django.forms import ModelForm
from .models import Expense
from django.contrib.auth.models import User

class ExpenseForm(ModelForm):
    class Meta:
        model = Expense
        fields = ('name','amount','category')
        
class UserRegistrationForm(ModelForm):
    password = forms.CharField(label='Pasword', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name']   

    def check_password(self):
        if self.cleaned_data['password'] != self.cleaned_data['password2']:
            raise forms.ValidationError('Hasła się nie zgadzają') 
        return self.cleaned_data['password']