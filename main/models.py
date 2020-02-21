from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.shortcuts import reverse
from django.utils import timezone
from django.utils.translation import gettext as _


class UserManager(BaseUserManager):
    def create_user(self, email, **kwargs):
        if not email:
            raise ValueError(_('User must have an email'))
        password = kwargs.get('password')
        if not password:
            raise ValueError(_('User must have a password'))
        user_obj = self.model(email=self.normalize_email(email))
        user_obj.set_password(password)

        user_obj.is_active = kwargs.get('active', False)
        user_obj.is_staff = kwargs.get('staff', False)
        user_obj.is_admin = kwargs.get('admin', False)
        user_obj.is_superuser = kwargs.get('superuser', False)

        user_obj.save(using=self._db)

        return user_obj

    def create_staff(self, email, password):
        return self.create_user(email, password=password, staff=True)

    def create_admin(self, email, password):
        return self.create_user(email, password=password, staff=True, admin=True)

    def create_superuser(self, email, password):
        return self.create_user(email, password=password, staff=True, admin=True, superuser=True)


class User(AbstractBaseUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def is_subscribed(self):
        subscriptions = Subscription.objects.filter(user=self)
        for subscription in subscriptions:
            if timezone.now() - subscription.started_at <= subscription.package.period:
                return True
        return False

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Package(models.Model):
    price = models.FloatField()
    period = models.DurationField()
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Subscription(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.package.name} started at {self.started_at}'


class Article(models.Model):
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=200)
    preview = models.TextField()
    content = models.TextField()
    image = models.ImageField()

    @property
    def image_url(self):
        return self.image.url

    @property
    def absolute_url(self):
        return reverse('article', kwargs={'pk': self.id, 'slug': self.slug})

    def __str__(self):
        return self.title
