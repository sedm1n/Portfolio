from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from django_email_verification import send_email

from .forms import UserCreationForm

User = get_user_model()

def register_view(request):
      if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                  user = form.save(commit=False)
                  user_email = form.cleaned_data.get('email')
                  user_name = form.cleaned_data.get('username')
                  user_password = form.cleaned_data.get('password1')
                  # crate new user
                  user = User.objects.create_user(user_name, user_email, user_password)
                  user.is_active = False
                  send_email(user)
                  
                  # return redirect('account:login')
      else:
            form = UserCreationForm()
      return render(request, 'account/registration/register.html', {'form': form})