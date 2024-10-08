
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput

User = get_user_model()

class UserCreationForm(UserCreationForm):

      class Meta:
            model = User
            fields = ('username', 'email', 'password1', 'password2')
      def __init__(self, *args, **kwargs):

            super(UserCreationForm, self).__init__(*args, **kwargs)

            self.fields['username'].help_text = ""
            self.fields['email'].label = "Your email address"
            self.fields['email'].required = True
            self.fields['password1'].help_text = ""

      def clean_email(self):
            email = self.cleaned_data.get('email').lower()
            if User.objects.filter(email=email).exists() and len(email) > 254:
                  raise forms.ValidationError("Email already exists or to long") 
            return email
      
class LoginForm(AuthenticationForm):
      username = forms.CharField(widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
      password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
