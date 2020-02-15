from django import forms
from django.contrib.auth.forms import AuthenticationForm as DjangoAuthenticatorForm
from django.contrib.auth.models import User


class InscriptionForm(forms.ModelForm):
    class Meta:
        model = User
        fields = []

    email = forms.EmailField(
        label='Email', required=True, widget=forms.TextInput(
            attrs={
                'type': 'email',
                'placeholder': 'Email',
                'class': 'inscriptionField',
            },
        ))
    email_confirmation = forms.EmailField(
        label="Confirmation de l'email", required=True, widget=forms.TextInput(
            attrs={
                'type': 'email',
                'placeholder': "Confirmation de l'email",
                'class': 'inscriptionField',
            },
        ))
    password = forms.CharField(
        label='Mot de passe', min_length=6, max_length=32,
        required=True,
        help_text='Le mot de passe doit contenir entre 6 et 32 caractères',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Mot de passe',
                'class': 'inscriptionField',
            },
        ))
    password_confirmation = forms.CharField(
        min_length=6, max_length=32, label='Confirmation du mot de passe',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Confirmation du mot de passe',
                'class': 'inscriptionField',
            },
        ))

    def clean(self):
        super().clean()

        email = self.cleaned_data.get('email')
        email_confirmation = self.cleaned_data.get('email_confirmation')
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')

        if email != email_confirmation:
            self._errors['email'] = 'Les emails ne correspondent pas'
        if password != password_confirmation:
            self._errors['password'] = 'Les mots de passe ne correspondent pas'
        if User.objects.filter(email=email):
            self._errors['email'] = 'Cet email est déjà utilisé'
        return self.cleaned_data

    def save(self, commit=True):
        return User.objects.create_user(self.cleaned_data['email'], password=self.cleaned_data['password'])


class ContactForm(forms.Form):
    last_name = forms.CharField(
        max_length=255, label='Nom', widget=forms.TextInput(
            attrs={
                'placeholder': 'Nom',
            },
        ))
    first_name = forms.CharField(
        max_length=255, label='Prénom', widget=forms.TextInput(
            attrs={
                'placeholder': 'Prénom',
            },
        ))
    email = forms.EmailField(
        label='Email', required=True, widget=forms.TextInput(
            attrs={
                'type': 'email',
                'placeholder': 'Email',
            },
        ))
    subject = forms.CharField(
        max_length=255, label='Objet', widget=forms.TextInput(
            attrs={
                'placeholder': 'Objet',
            },
        ))
    message = forms.CharField(
        label='Entrez votre message', widget=forms.Textarea(
            attrs={
                'placeholder': 'Ecrivez votre message',
            },
        ))


class AuthenticationForm(DjangoAuthenticatorForm):
    username = forms.EmailField(
        label='Email', required=True, widget=forms.TextInput(
            attrs={
                'type': 'email',
                'placeholder': 'Email',
                'class': 'inscriptionField',
            },
        ))
    password = forms.CharField(
        min_length=6, max_length=32, label='Mot de passe',
        help_text='Le mot de passe doit contenir entre 6 et 32 caractères',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Mot de passe',
                'class': 'inscriptionField',
            },
        ))
