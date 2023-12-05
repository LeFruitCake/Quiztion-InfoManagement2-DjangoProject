from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import FlashcardSets, Flashcard, PremiumAccount

class LoginForm(forms.Form):
    username = forms.CharField(max_length =65)
    password = forms.CharField(max_length=65, widget = forms.PasswordInput)

    
class RegisterForm(UserCreationForm):
    class Meta:
        model=User
        fields = ['username','email','password1','password2'] 

class CardSetForm(forms.ModelForm):
    class Meta:
        model = FlashcardSets
        fields = ['setTitle']

class FlashcardForm(ModelForm):
    class Meta:
        model = Flashcard
        fields = ['question', 'answer']

class PremiumForm(ModelForm):
    class Meta:
        model = PremiumAccount
        fields = ['isPremium']
