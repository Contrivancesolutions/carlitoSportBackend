from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, FormView

from main.forms import ContactForm, LoginForm, RegisterForm
from main.models import Article, Package, Subscription


class HomeView(TemplateView):
    template_name = 'main/index.html'


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


class LoginView(UserPassesTestMixin, FormView):
    template_name = 'main/login.html'
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


class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'main/resetPassword.html'


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'main/resetPasswordDone.html'


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'main/confirmResetPassword.html'


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'main/resetPasswordComplete.html'


class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    template_name = 'main/logged_out.html'


class SubscriptionView(LoginRequiredMixin, CreateView):
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        context = {'packages': Package.objects.all()}
        return render(request, 'main/subscription.html', context)

    def post(self, request, *args, **kwargs):
        context = {'packages': Package.objects.all()}

        package_id = request.POST.get('package_id', 0)
        package = get_object_or_404(Package.objects, id=package_id)
        if package:
            Subscription(user=self.request.user, package=package).save()
            return redirect('pronos')
        return render(request, 'main/subscription.html', context)


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


class ArticleView(DetailView):
    template_name = 'main/article.html'
    model = Article

    def get(self, *args, **kwargs):
        self.entity = self.get_object()
        obj_url = self.entity.absolute_url
        if self.request.path != obj_url:
            return HttpResponsePermanentRedirect(obj_url)
        return super().get(*args, **kwargs)


class BonusView(TemplateView):
    template_name = 'main/bonus.html'


class CertificationView(TemplateView):
    template_name = 'main/certification.html'


class FaqView(TemplateView):
    template_name = 'main/FAQ.html'


class PronosView(TemplateView):
    template_name = 'main/pronos.html'
