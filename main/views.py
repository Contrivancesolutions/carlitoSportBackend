from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from main.forms import AuthenticationForm, ContactForm, InscriptionForm
from main.models import Abonnement, User


def homepage(request):
    return render(request=request, template_name='main/index.html')


@user_passes_test(lambda user: user.is_anonymous, login_url='/')
def register(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save()

            login(request, user)
            abonnement = Abonnement(user=user)
            abonnement.save()
            return redirect('main:register2')
    else:
        form = InscriptionForm().as_p()
    return render(request, 'main/inscription.html', context={'form': form})


@login_required
def logout_request(request):
    logout(request)
    return redirect('main:homepage')


@user_passes_test(lambda user: user.is_anonymous, login_url='/')
def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=email, password=password)
            if user:
                login(request, user)
                return redirect('main:homepage')
            else:
                messages.error(request, 'Les donnés entrées ne correspondent à aucun client')
        else:
            messages.error(request, 'Mot de passe ou email incorrect')
    else:
        form = AuthenticationForm().as_p()
    return render(request, 'main/login.html', context={'form': form})


def register2(request):
    return render(request, 'main/inscription2.html')


def bonus(request):
    return render(request, 'main/bonus.html')


def certification(request):
    return render(request, 'main/certification.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request, request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            message = form.cleaned_data.get('message')

            content = f'De {last_name} {first_name}\n{message}'

            send_mail(
                form.cleaned_data.get('subject'), content,
                form.cleaned_data.get('email'), ['azimgivron@gmail.com'],
            )
        else:
            messages.error(request, 'Les données entrées ne correspondent pas aux formats attendus')
    form = ContactForm().as_p()
    return render(request, 'main/contact.html', context={'form': form})


def news(request):
    return render(request, 'main/news.html')


def faq(request):
    return render(request, 'main/FAQ.html')


def pronos(request):
    return render(request, 'main/pronos.html')


def article1(request):
    return render(request, 'main/article1.html')


def article2(request):
    return render(request, 'main/article2.html')


def article3(request):
    return render(request, 'main/article3.html')


def article4(request):
    return render(request, 'main/article4.html')


def article5(request):
    return render(request, 'main/article5.html')


def article6(request):
    return render(request, 'main/article6.html')


def article7(request):
    return render(request, 'main/article7.html')


def article8(request):
    return render(request, 'main/article8.html')


def article9(request):
    return render(request, 'main/article9.html')


def article10(request):
    return render(request, 'main/article10.html')
