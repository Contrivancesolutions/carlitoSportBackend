from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import InscriptionForm, AuthenticationForm, ContactForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Abonnement
User = get_user_model()


def homepage(request):
    return render(request=request, template_name="main/index.html")


def register(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if User.object.filter(email=data['email']) == None:
                if data['email'] == data['emailConf']:
                    if data['password1'] == data['password2']:
                        user = form.save()
                        login(request, user)
                        abonnement = Abonnement(user=user)
                        abonnement.save()
                        return redirect("main:register2")
                    else:
                        messages.error(
                            request, 'Les mots de passe ne correspondent pas')
                else:
                    messages.error(request, 'Les emails ne correspondent pas')
            else:
                messages.error(request, 'Cet email est déjà utilisé')
        else:
            messages.error(
                request, 'Les informations ne correspondent pas au format demandé')

    form = InscriptionForm().as_p()
    return render(request, "main/inscription.html", context={"form": form}) if not(request.user.is_authenticated) else redirect("main:homepage")


def logout_request(request):
    logout(request)
    return redirect("main:homepage")


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("main:homepage")
            else:
                messages.error(
                    request, "Les donnés entrées ne correspondent à aucun client")
        else:
            messages.error(request, "Mot de passe ou email incorrect")

    form = AuthenticationForm().as_p()
    return render(request, "main/login.html", context={"form": form}) if not(request.user.is_authenticated) else redirect("main:homepage")


def register2(request):
    return render(request, "main/inscription2.html")


def bonus(request):
    return render(request, "main/bonus.html")


def certification(request):
    return render(request, "main/certification.html")


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request, data=request.POST)
        if form.is_valid():
            firstName = form.cleaned_data.get('firstName')
            lastName = form.cleaned_data.get('lastName')
            email = form.cleaned_data.get('email')
            subject = form.cleaned_data.get('subject')
            message = form.cleaned_data.get('message')
            msg = "De {} {}\n{}".format(lastName, firstName, message)

            send_mail(subject, message, EMAIL_HOST_USER,
                      ['azimgivron@gmail.com'])
        else:
            messages.error(
                request, "Les données entrées ne correspondent pas aux formats attendus")
    form = ContactForm().as_p()
    return render(request, "main/contact.html", context={"form": form})


def news(request):
    return render(request, "main/news.html")


def faq(request):
    return render(request, "main/FAQ.html")


def pronos(request):
    return render(request, "main/pronos.html")


def article1(request):
    return render(request, "main/article1.html")


def article2(request):
    return render(request, "main/article2.html")


def article3(request):
    return render(request, "main/article3.html")


def article4(request):
    return render(request, "main/article4.html")


def article5(request):
    return render(request, "main/article5.html")


def article6(request):
    return render(request, "main/article6.html")


def article7(request):
    return render(request, "main/article7.html")


def article8(request):
    return render(request, "main/article8.html")


def article9(request):
    return render(request, "main/article9.html")


def article10(request):
    return render(request, "main/article10.html")
