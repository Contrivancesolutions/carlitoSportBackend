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
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from main import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='homepage'),
    path('i18n/<lang>', views.LangView.as_view(), name='i18n'),
    path('inscription/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('subscription/', views.SubscriptionView.as_view(), name='subscription'),
    path('activate/<uidb64>/<token>', views.ActivateAccountView.as_view(), name='activate'),
    path('password-reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path(
        'password-reset-confirm/<uidb64>/<token>/',
        views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm',
    ),
    path('password-reset-complete/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('bonus/', views.BonusView.as_view(), name='bonus'),
    path('certification/', views.CertificationView.as_view(), name='certification'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('faq/', views.FaqView.as_view(), name='faq'),
    path('pronos', views.PronosView.as_view(), name='pronos'),
    path('news', views.NewsView.as_view(), name='news'),
    path('article/<int:pk>-<str:slug>', views.ArticleView.as_view(), name='article'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
