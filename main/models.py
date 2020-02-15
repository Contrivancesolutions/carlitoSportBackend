from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, active=True, staff=False, admin=False, superuser=False):
        if not email:
            raise ValueError("User must have an email")
        if password is None:
            raise ValueError("User must have a password")
        user_obj = self.model(
            email=self.normalize_email(email)
        )
        user_obj.set_password(password)

        user_obj.is_active = active
        user_obj.is_staff = staff
        user_obj.is_admin = admin
        user_obj.is_superuser = superuser

        user_obj.save(using=self._db)

        return user_obj

    def create_staff(self, email, password):
        return self.create_user(email, password=password, staff=True)

    def create_admin(self, email, password):
        return self.create_user(email, password=password, staff=True, admin=True)

    def create_superuser(self, email, password):
        return self.create_user(email, password=password, staff=True, admin=True, superuser=True)


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Abonnement(models.Model):
    class AbonnementType(models.IntegerChoices):
        package1 = 1
        package2 = 2
        package3 = 3
        package4 = 4

    hasAnAbonnement = models.BooleanField(default=False)
    abonnementType = models.IntegerField(
        choices=AbonnementType.choices, null=True)
    timestamp = models.DateTimeField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.AbonnementType
