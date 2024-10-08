from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from django_email_verification import send_email

from .forms import LoginForm, UserCreationForm, UserUpdateForm

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
                  
                  return redirect('account:email_verification_sent')
      else:
            form = UserCreationForm()
      return render(request, 'account/registration/register.html', {'form': form})

def user_login_view(request):

      form = LoginForm(request.POST)
            
      if request.user.is_authenticated:
            return redirect('shop:products')
      if request.method == 'POST':

            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                  login(request, user)
                  return redirect('account:dashboard')
            else:
                  messages.info(request, 'Username or password is incorrect')
                  redirect('account:login')

      context = {'form': form}

      return render(request, 'account/login/login.html', context)

@login_required
def user_logout_view(request):
      logout(request)
      return redirect('account:login')

@login_required
def dashboard_view(request):
      
      return render(request, 'account/dashboard/dashboard.html')

@login_required
def profile_manegment_view(request):
      form = UserUpdateForm(request.POST, instance=request.user)
      if request.method == 'POST':
            
            if form.is_valid():
                  form.save()
                  messages.success(request, 'Profile updated successfully')
                  return redirect('account:dashboard')

      context = {'form': form}
      return render(request, 'account/dashboard/profile-management.html', context)

@login_required
def delete_user_view(request):
      user = User.objects.get(id=request.user.id)
      if request.method == 'POST':
            user.delete()
            user.save()
      

      messages.success(request, 'Account deleted successfully')
      return render(request, 'account/login/login.html')