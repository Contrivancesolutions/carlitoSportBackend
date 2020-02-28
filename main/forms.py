from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext as _
from main.models import User


class RegisterForm(forms.Form):
    email = forms.EmailField(
        label=_('Email'), required=True, widget=forms.TextInput(
            attrs={
                'type': 'email',
                'placeholder': _('Email'),
                'class': 'inscriptionField',
            },
        ))
    email_confirmation = forms.EmailField(
        label=_("Confirmation de l'email"), required=True, widget=forms.TextInput(
            attrs={
                'type': 'email',
                'placeholder': _("Confirmation de l'email"),
                'class': 'inscriptionField',
            },
        ))
    password = forms.CharField(
        label=_('Mot de passe'), min_length=6, max_length=32,
        required=True,
        help_text=_('Le mot de passe doit contenir entre 6 et 32 caractères'),
        widget=forms.PasswordInput(
            attrs={
                'placeholder': _('Mot de passe'),
                'class': 'inscriptionField',
            },
        ))
    password_confirmation = forms.CharField(
        min_length=6, max_length=32, label=_('Confirmation du mot de passe'),
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': _('Confirmation du mot de passe'),
                'class': 'inscriptionField',
            },
        ))

    def clean(self):
        super().clean()

        email = self.cleaned_data.get('email')
        email_confirmation = self.cleaned_data.get('email_confirmation')
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')

        try:
            validate_email(email)
        except ValidationError:
            self.add_error('email', _('Veuillez insérer un email valide'))

        if email != email_confirmation:
            self.add_error('email', _('Les emails ne correspondent pas'))
        if password != password_confirmation:
            self.add_error('password', _('Les mots de passe ne correspondent pas'))
        if User.objects.filter(email=email):
            self.add_error('email', _('Cet email est déjà utilisé'))

        return self.cleaned_data

    def save(self, commit=True):
        return User.objects.create_user(self.cleaned_data['email'], password=self.cleaned_data['password'])


class ContactForm(forms.Form):
    last_name = forms.CharField(
        max_length=255, label=_('Nom'), widget=forms.TextInput(
            attrs={
                'placeholder': _('Nom'),
                'class': 'contact-form',
            },
        ))
    first_name = forms.CharField(
        max_length=255, label=_('Prénom'), widget=forms.TextInput(
            attrs={
                'placeholder': _('Prénom'),
                'class': 'contact-form',
            },
        ))
    email = forms.EmailField(
        label=_('Email'), required=True, widget=forms.TextInput(
            attrs={
                'type': 'email',
                'placeholder': _('Email'),
                'class': 'contact-form',
            },
        ))
    subject = forms.CharField(
        max_length=255, label=_('Objet'), widget=forms.TextInput(
            attrs={
                'placeholder': _('Objet'),
                'class': 'contact-form',
            },
        ))
    message = forms.CharField(
        label=_('Entrez votre message'), widget=forms.Textarea(
            attrs={
                'placeholder': _('Ecrivez votre message'),
                'class': 'contact-form',
            },
        ))

    def clean(self):
        super().clean()

        email = self.cleaned_data.get('email')
        try:
            validate_email(email)
        except ValidationError:
            self.add_error('email', _('Veuillez insérer un email valide'))


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label=_('Email'), required=True, widget=forms.TextInput(
            attrs={
                'type': 'email',
                'placeholder': _('Email'),
                'class': 'inscriptionField',
            },
        ))
    password = forms.CharField(
        min_length=6, max_length=32, label=_('Mot de passe'),
        widget=forms.PasswordInput(
            attrs={
                'placeholder': _('Mot de passe'),
                'class': 'inscriptionField',
            },
        ))

    def clean(self):
        super().clean()
        email = self.cleaned_data.get('username')
        try:
            validate_email(email)
        except ValidationError:
            self.add_error('email', _('Veuillez insérer un email valide'))
        return self.cleaned_data
