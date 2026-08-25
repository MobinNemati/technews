"""Class-based views for authentication and account recovery."""

from django.contrib import messages
from django.contrib.auth import get_user_model, logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, RedirectView

from accounts.forms import EmailOrUsernameAuthenticationForm, SignUpForm


User = get_user_model()

HOME_URL = reverse_lazy('website:index')


class FormErrorsAsMessagesMixin:
    """Report form errors through ``django.contrib.messages``.

    The account templates only render the message list, so without this the
    validation errors would never reach the visitor.
    """

    def form_invalid(self, form):
        for errors in form.errors.values():
            for error in errors:
                messages.error(self.request, error)
        return super().form_invalid(form)


class AnonymousRequiredMixin:
    """Send visitors who are already signed in somewhere else."""

    redirect_authenticated_to = HOME_URL

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.redirect_authenticated_to)
        return super().dispatch(request, *args, **kwargs)


class UserLoginView(FormErrorsAsMessagesMixin, auth_views.LoginView):
    """Sign in with a username or an e-mail address."""

    template_name = 'accounts/login.html'
    form_class = EmailOrUsernameAuthenticationForm
    redirect_authenticated_user = True
    next_page = HOME_URL


class UserLogoutView(LoginRequiredMixin, RedirectView):
    """Sign the current user out.

    ``RedirectView`` is used instead of ``auth_views.LogoutView`` because the
    navbar and the footer link here with a plain anchor, and ``LogoutView``
    only accepts POST since Django 5.0.
    """

    url = HOME_URL
    permanent = False

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class UserSignUpView(AnonymousRequiredMixin, FormErrorsAsMessagesMixin, CreateView):
    """Register a new account."""

    template_name = 'accounts/signup.html'
    form_class = SignUpForm
    success_url = HOME_URL


class UserPasswordResetView(auth_views.PasswordResetView):
    """Mail a reset link, or state that the address is unknown."""

    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    success_url = reverse_lazy('accounts:password_reset_done')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        if not User.objects.filter(email__iexact=email).exists():
            return render(self.request, 'accounts/password_reset_failed.html')
        return super().form_valid(form)


class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')


class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'
