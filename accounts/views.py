from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.contrib.sites.models import Site



def login_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username_or_email = request.POST.get('username')
            password = request.POST.get('password')

            try:
                user = User.objects.get(email=username_or_email)
            except User.DoesNotExist:
                user = None

            if user is not None:
                user = authenticate(request, username=user.username, password=password)
            else:
                user = authenticate(request, username=username_or_email, password=password)

            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, 'Invalid username or password')
        return render(request, 'accounts/login.html')
    else:
        return redirect('/') 


@login_required()
def logout_view(request):
    logout(request)
    return redirect('/')


def signup_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirm_password = request.POST.get('password2')

            if password != confirm_password:
                messages.error(request, 'Password and Confirm Password do not match.')
            
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email already exists.')
                else:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    return redirect('/')

        return render(request, 'accounts/signup.html')
    else:
        return redirect('/')
    
class UserPasswordResetView(auth_views.PasswordResetView):
    template_name = 'accounts/password_reset.html'
    success_url = reverse_lazy('accounts:password_reset_done')
    email_template_name = 'accounts/password_reset_email.html'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        user_exists = User.objects.filter(email=email).exists()

        if user_exists:
            return super().form_valid(form)
        else:
            return render(self.request, 'accounts/password_reset_failed.html')
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_site = Site.objects.get_current()
        context['protocol'] = 'http' if self.request.is_secure() else 'https'
        context['domain'] = current_site.domain
        return context




class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')


class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'
