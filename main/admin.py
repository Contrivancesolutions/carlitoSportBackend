from django.contrib import admin
from main.models import Abonnement, User

class UserAdmin(admin.ModelAdmin):
    search_fields = ['email']

    class Meta:
        model = User


admin.site.register(User, UserAdmin)

admin.site.register(Abonnement)
