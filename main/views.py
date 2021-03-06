from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils import translation
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.translation import gettext as _
from django.views.generic import DetailView, ListView, TemplateView, View
from django.views.generic.edit import CreateView

from main import conf
from main.forms import ContactForm, LoginForm, RegisterForm
from main.models import Article, Package, NewsLetterUser, Subscription, User
from main.payement import make_payement
from main.tokens import account_activation_token
from main.utils import FormErrorsView


class HomeView(View):
    def get(self, request, *args, **kwargs):
        articles = Article.objects.all().order_by('-id')[:3]
        context = {'packages': Package.objects.all(), 'articles': articles}
        return render(request, 'main/index.html', context)


class LangView(View):
    def get(self, request, lang):
        if lang in conf.AVAILABLE_LANGUAGES:
            translation.activate(lang)
            request.session[translation.LANGUAGE_SESSION_KEY] = lang
        return redirect('homepage')


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

        messages.success(self.request, _('Votre compte a bien été créé'))
        return redirect('homepage')


class RegisterView(UserPassesTestMixin, FormErrorsView):
    template_name = 'auth/register.html'
    form_class = RegisterForm

    def handle_no_permission(self):
        return redirect('homepage')

    def get_initial(self):
        return {
            'email': self.request.GET.get('email', ''),
            'email_confirmation': self.request.GET.get('email_confirmation', '')
        }

    def test_func(self):
        return self.request.user.is_anonymous

    def form_valid(self, form):
        user = form.save()

        if form.cleaned_data['subscribed_newsletter']:
            NewsLetterUser(email=user.email).save()

        message = render_to_string('mails/activate_account.html', {
            'user': user,
            'domain': get_current_site(self.request).domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })


        email = EmailMessage(_(
            'Un email contenant le lien d\'activation de votre compte vous a été envoyé'), message, to=[user.email])
        email.send()
        # Don't log in automatically anymore, the user needs to validate
        # their account first
        redirect_to = self.request.GET.get('to', 'subscription')
        messages.success(self.request, _('Finalise la création de ton compte via l\'emails que nous t\'avons envoyé.'))
        return redirect(redirect_to)


class LoginView(UserPassesTestMixin, FormErrorsView):
    template_name = 'auth/login.html'
    form_class = LoginForm

    def get(self, request, **kwargs):
        ctx = super().get_context_data(**kwargs)
        return render(request, 'auth/login.html', ctx)

    def handle_no_permission(self):
        return redirect('homepage')

    def test_func(self):
        return self.request.user.is_anonymous

    def form_valid(self, form):
        slug = self.request.POST.get('slug', '')

        email = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=email, password=password)

        if user:
            login(self.request, user)
            if slug=='':
                return redirect('homepage')
            else:
                try:
                    article = get_object_or_404(Article.objects, slug=slug)
                    obj_url = article.absolute_url
                    return redirect(obj_url)
                except Exception as e:
                    pass
        return super().form_invalid(form)


class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'auth/reset_password.html'

    def get(self, request):
        form = self.get_form()
        for field in form.fields.values():
            field.widget.attrs['class'] = 'inscriptionField'

        return render(request, self.template_name, context={
            'form': form
        })

    def form_valid(self, form):
        messages.info(self.request, _(
            'Un email contenant les instructions pour réinitialiser votre mot de passe vous a été envoyé'))
        return super().form_valid(form)


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'auth/confirm_reset_password.html'

    def get(self, request):
        form = self.get_form()
        for field in form.fields.values():
            field.widget.attrs['class'] = 'inscriptionField'

        return render(request, self.template_name, context={
            'form': form
        })

    def form_valid(self, form):
        messages.info(self.request, _('Votre mot de passe a bien été mis à jour.'))
        return redirect('login')


class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    def get(self, request):
        messages.info(request, _('Vous avez bien été deconnecté.'))
        return redirect('homepage')


class SubscriptionView(LoginRequiredMixin, CreateView):
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        context = {'packages': Package.objects.all()}
        return redirect('homepage') if request.user.is_subscribed else render(request, 'main/subscription.html', context)


class PaymentView(LoginRequiredMixin, FormErrorsView):
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        try:
            package_id = request.GET.get('package_id', 0)
            package = get_object_or_404(Package.objects, id=package_id)
        except Exception as e:
            return redirect('homepage') if request.user.is_subscribed else redirect('subscription')

        context = {'package': package, 'form': self.get_form()}
        return render(request, 'main/payment.html', context)

    def form_valid(self, form):
        context = {'packages': Package.objects.all()}

        try:
            package_id = request.POST.get('package_id', 0)
            package = get_object_or_404(Package.objects, id=package_id)
            if package and make_payement(self.request.user, package):
                Subscription(user=self.request.user, package=package).save()
                return redirect('pronos')
        except Exception as e:
            pass

        return render(request, 'main/payment.html', context)


class ContactView(FormErrorsView):
    template_name = 'main/contact.html'
    form_class = ContactForm

    def get_initial(self):
        if not self.request.user.is_anonymous:
            user = self.request.user
            return {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
            }

    def form_valid(self, form):
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        message = form.cleaned_data.get('message')

        content = f'De {last_name} {first_name}\n{message}'

        send_mail(
            form.cleaned_data.get('subject'), content,
            form.cleaned_data.get('email'), ['azimgivron@gmail.com'],
        )
        return redirect('contact')


class NewsView(ListView):
    template_name = 'main/news.html'
    queryset = Article.objects.all().order_by('-id')


class ArticleView(DetailView):
    template_name = 'main/article.html'
    model = Article

    def get(self, *args, **kwargs):
        self.entity = self.get_object()
        obj_url = self.entity.absolute_url
        user = self.request.user

        if user.is_authenticated:
            if self.request.path != obj_url:
                return HttpResponsePermanentRedirect(obj_url)
            return super().get(*args, **kwargs)
        else:
            messages.info(self.request, _('Connecte toi et accède à l\'entièreté de nos articles de presse!'))
            redirect_to = self.request.GET.get('to', 'login')
            return redirect(redirect_to, slug=self.entity.slug)


class BonusView(TemplateView):
    template_name = 'main/bonus.html'


class CertificationView(TemplateView):
    template_name = 'main/certification.html'


class FaqView(TemplateView):
    template_name = 'main/FAQ.html'


class PronosView(TemplateView):
    template_name = 'main/pronos.html'

    def get(self, request):
        user = self.request.user

        if user.is_authenticated and user.is_subscribed:
            return super().get(request)
        elif user.is_authenticated and not user.is_subscribed:
            messages.info(self.request, _('Abonne toi pour consulter les pronos!'))
            redirect_to = self.request.GET.get('to', 'subscription')
            return redirect(redirect_to)
        else:
            messages.info(self.request, _('Accéde aux pronos en créant un compte!'))
            redirect_to = self.request.GET.get('to', 'register')
            return redirect(redirect_to)
