from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
User = get_user_model()

class InscriptionForm(forms.Form):
	email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={"type": "email", "placeholder": "Email", "class": "inscriptionField"}), required=True)
	emailConf = forms.EmailField(label="Confirmation de l'email", widget=forms.TextInput(attrs={"type": "email", "placeholder": "Confirmation de l'email", "class": "inscriptionField"}), required=True)
	password1 = forms.CharField(min_length=6, max_length=32, label="Mot de passe", widget=forms.PasswordInput(attrs={"placeholder": "Mot de passe", "class": "inscriptionField"}), help_text="Le mot de passe doit contenir entre 6 et 32 caractères")
	password2 = forms.CharField(min_length=6, max_length=32, label="Confirmation du mot de passe", widget=forms.PasswordInput(attrs={"placeholder": "Confirmation du mot de passe", "class": "inscriptionField"}))

	def save(self, commit=True):
		return User.objects.create_user(self.cleaned_data['email'], password = self.cleaned_data['password1'])

class ContactForm(forms.Form):
	lastName = forms.CharField(max_length=255, label="Nom", widget=forms.TextInput(attrs={"placeholder": "Nom"}))
	fisrtName = forms.CharField(max_length=255, label="Prénom", widget=forms.TextInput(attrs={"placeholder": "Prénom"}))
	email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={"type": "email", "placeholder": "Email"}), required=True)
	subject = forms.CharField(max_length=255, label="Objet", widget=forms.TextInput(attrs={"placeholder": "Objet"}))
	message = forms.CharField(label="Entrez votre message", widget=forms.Textarea(attrs={"placeholder": "Ecrivez votre message"}))


class AuthenticationForm(AuthenticationForm):
	username = forms.EmailField(label="Email", widget=forms.TextInput(attrs={"type": "email", "placeholder": "Email", "class": "inscriptionField"}), required=True)
	password = forms.CharField(min_length=6, max_length=32, label="Mot de passe", widget=forms.PasswordInput(attrs={"placeholder": "Mot de passe", "class": "inscriptionField"}), help_text="Le mot de passe doit contenir entre 6 et 32 caractères")