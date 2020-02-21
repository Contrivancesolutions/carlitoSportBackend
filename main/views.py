from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import DetailView, ListView, TemplateView, View
from django.views.generic.edit import CreateView, FormView

from main.forms import ContactForm, LoginForm, RegisterForm
from main.models import Article, Package, Subscription, User
from main.tokens import account_activation_token


class HomeView(View):
    def get(self, request, *args, **kwargs):
        articles = Article.objects.all().order_by('-id')[:3]
        context = {'packages': Package.objects.all(), 'articles': articles}
        return render(request, 'main/index.html', context)


class ActivateAccountView(View):
    def get(self, request, uid64, token):
        uid = force_bytes(urlsafe_base64_decode(uid64))
        try:
            user = User.objects.get(id=uid)
        except Exception:
            user = None

        if user and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)

        # TODO: handle the case when the token is wrong, display some kind of 404 error page?
        return redirect('homepage')


class RegisterView(UserPassesTestMixin, FormView):
    template_name = 'auth/register.html'
    form_class = RegisterForm
    success_url = 'subscription'

    def handle_no_permission(self):
        return redirect('homepage')

    def test_func(self):
        return self.request.user.is_anonymous

    def form_valid(self, form):
        user = form.save()

        message = render_to_string('mails/activate_account.html', {
            'user': user,
            'domain': get_current_site(self.request).domaion,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
            'token': account_activation_token.make_token(user),
        })

        email = EmailMessage('Activate Your Account', message, to=[user.email])
        email.send()

        # Don't log in automatically anymore, the user needs to validate
        # their account first
        return super().form_valid(form)


class LoginView(UserPassesTestMixin, FormView):
    template_name = 'auth/login.html'
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
    template_name = 'auth/reset_password.html'


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'auth/reset_password_done.html'


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'auth/confirm_reset_password.html'


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'auth/reset_password_complete.html'


class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    template_name = 'auth/logged_out.html'


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
