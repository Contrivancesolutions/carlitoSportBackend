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
from django.contrib.auth import views as auth_views
from django.urls import path
from main import views

app_name = 'main'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('inscription/', views.register, name='register'),
    path('logout/', views.logout_request, name='logout'),
    path('login/', views.login_request, name='login'),
    path('inscription2/', views.register2, name='register2'),
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
    path('contact/', views.contact, name='contact'),
    path('faq/', views.faq, name='faq'),
    path('pronos', views.pronos, name='pronos'),
    path('news', views.news, name='news'),
    path('article1/', views.article1, name='article1'),
    path('article2/', views.article2, name='article2'),
    path('article3/', views.article3, name='article3'),
    path('article4/', views.article4, name='article4'),
    path('article5/', views.article5, name='article5'),
    path('article6/', views.article6, name='article6'),
    path('article7/', views.article7, name='article7'),
    path('article8/', views.article8, name='article8'),
    path('article9/', views.article9, name='article9'),
    path('article10/', views.article10, name='article10'),
]
