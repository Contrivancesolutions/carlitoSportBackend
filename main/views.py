from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LogoutView as AuthLogoutView
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.views.generic import View, ListView
from django.views.generic.edit import FormView

from main.forms import ContactForm, LoginForm, RegisterForm
from main.models import Abonnement, Article, User


def homepage(request):
    return render(request, template_name='main/index.html')


class RegisterView(UserPassesTestMixin, FormView):
    template_name = 'main/register.html'
    form_class = RegisterForm
    success_url = 'subscription'

    def handle_no_permission(self):
        return redirect('homepage')

    def test_func(self):
        return self.request.user.is_anonymous

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class LogoutView(LoginRequiredMixin, AuthLogoutView):
    template_name = 'main/logged_out.html'


class LoginView(UserPassesTestMixin, FormView):
    template_name = 'main/login.html'
    raise_exception = False
    form_class = LoginForm
    success_url = 'homepage'

    def handle_no_permission(self):
        return redirect('homepage')

    def test_func(self):
        return self.request.user.is_anonymous

    def form_valid(self, form):
        email = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=email, password=password)
        if user:
            login(self.request, user)
            return super().form_valid(form)
        return super().form_invalid(form)


@login_required
def subscription(request):
    if request.method == 'POST':
        abonnement = Abonnement(user=request.user)
        abonnement.save()
        return redirect('homepage')
    else:
        return render(request, 'main/subscription.html')


def bonus(request):
    return render(request, 'main/bonus.html')


def certification(request):
    return render(request, 'main/certification.html')


class ContactView(FormView):
    template_name = 'main/contact.html'
    form_class = ContactForm
    success_url = 'homepage'

    def form_valid(self, form):
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        message = form.cleaned_data.get('message')

        content = f'De {last_name} {first_name}\n{message}'

        send_mail(
            form.cleaned_data.get('subject'), content,
            form.cleaned_data.get('email'), ['azimgivron@gmail.com'],
        )
        return super().form_valid(form)


class NewsView(ListView):
    template_name = 'main/news.html'
    queryset = Article.objects.all().order_by('-id')


def article(request, article_id: int, article_slug: str):
    article = get_object_or_404(Article, id=article_id)
    if article.slug != article_slug:
        return redirect('article', *(article_id, article.slug), permanent=True)

    return render(request, 'main/article.html', {
        'article': article
    })


def faq(request):
    return render(request, 'main/FAQ.html')


def pronos(request):
    return render(request, 'main/pronos.html')
