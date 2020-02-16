from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from django.template import RequestContext

from main.forms import AuthenticationForm, ContactForm, InscriptionForm
from main.models import Abonnement, Article, User


def homepage(request):
    return render(request, template_name='main/index.html')


@user_passes_test(lambda user: user.is_anonymous, login_url='/')
def register(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main:subscription')
    else:
        form = InscriptionForm().as_p()
    return render(request, 'main/inscription.html', {'form': form})


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
    return render(request, 'main/login.html', {'form': form})

@login_required
def subscription(request):
    if request.method == 'POST':
        abonnement = Abonnement(user=request.user)
        abonnement.save()
        return redirect('main:homepage')
    else:
        return render(request, 'main/subscription.html')


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
    return render(request, 'main/contact.html', {'form': form})


def news(request):
    articles = Article.objects.all().order_by('-id')
    return render(request, 'main/news.html', {
        'articles': articles
    })


def article(request, article_id: int, article_slug: str):
    article = get_object_or_404(Article, id=article_id)
    if article.slug != article_slug:
        return redirect('main:article', *(article_id, article.slug), permanent=True)

    return render(request, 'main/article.html', {
        'article': article
    })


def faq(request):
    return render(request, 'main/FAQ.html')


def pronos(request):
    return render(request, 'main/pronos.html')

