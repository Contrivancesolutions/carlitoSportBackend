"""carlitoSport URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.urls import path
from main import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('inscription/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('subscription/', views.subscription, name='subscription'),
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(template_name='main/resetPassword.html'),
        name='password_reset',
    ),
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name='main/resetPasswordDone.html'),
        name='password_reset_done',
    ),
    path(
        'password-reset-confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='main/confirmResetPassword.html'),
        name='password_reset_confirm',
    ),
    path(
        'password-reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name='main/resetPasswordComplete.html'),
        name='password_reset_complete',
    ),
    path('bonus/', views.bonus, name='bonus'),
    path('certification/', views.certification, name='certification'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('faq/', views.faq, name='faq'),
    path('pronos', views.pronos, name='pronos'),
    path('news', views.NewsView.as_view(), name='news'),
    path('article/<int:article_id>-<str:article_slug>', views.article, name='article'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
