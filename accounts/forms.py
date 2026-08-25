"""Forms backing the account views.

The account templates hand-write their ``<input>`` elements instead of
rendering ``{{ form }}``, so the field names below deliberately mirror the
``name`` attributes used in ``templates/accounts/``.
"""

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


User = get_user_model()


class EmailOrUsernameAuthenticationForm(AuthenticationForm):
    """Let visitors sign in with either their username or their e-mail."""

    error_messages = {
        **AuthenticationForm.error_messages,
        'invalid_login': 'Invalid username or password',
    }

    def clean(self):
        credential = self.cleaned_data.get('username')
        if credential and '@' in credential:
            # Only look up an e-mail when the input can be one; a username
            # stays the default credential and costs no extra query.
            username = (
                User.objects.filter(email__iexact=credential)
                .values_list(User.USERNAME_FIELD, flat=True)
                .first()
            )
            if username:
                self.cleaned_data['username'] = username
        return super().clean()


class SignUpForm(forms.ModelForm):
    """Create a user account from the sign-up template."""

    password = forms.CharField(strip=False, widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Confirm password',
        strip=False,
        widget=forms.PasswordInput,
    )

    class Meta:
        model = User
        fields = ('username', 'email')
        field_classes = {'username': UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ``User.email`` is optional on the model, but signing in by e-mail
        # and resetting a password both depend on it.
        self.fields['email'].required = True

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError('Email already exists.')
        return email

    def clean_password2(self):
        password2 = self.cleaned_data['password2']
        if self.cleaned_data.get('password') != password2:
            raise ValidationError(
                'Password and Confirm Password do not match.',
            )
        return password2

    def _post_clean(self):
        # Runs once the instance is populated, so the password can be checked
        # against the submitted username and e-mail.
        super()._post_clean()
        password = self.cleaned_data.get('password')
        if password:
            try:
                validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error('password', error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
