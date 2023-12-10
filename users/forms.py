from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import ClearableFileInput
from .models import FlashcardSets, Flashcard, PremiumAccount, ProfilePhoto

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


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
    def __init__(self, *args, **kwargs):
        super(UpdateProfileForm, self).__init__(*args, **kwargs)
        # Disable the 'username' field
        self.fields['username'].widget.attrs['disabled'] = True

class CustomClearableFileInput(ClearableFileInput):
    clearable = False

class ProfilePhotoForm(forms.ModelForm):
    class Meta:
        model = ProfilePhoto
        fields = ['image']
        widgets = {'image': CustomClearableFileInput}
    def __init__(self, *args, **kwargs):
        super(ProfilePhotoForm, self).__init__(*args, **kwargs)
        # Set the image field as not required
        self.fields['image'].required = False
