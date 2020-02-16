from django.contrib import admin
from main.models import Abonnement, Article, User

class UserAdmin(admin.ModelAdmin):
    search_fields = ['email']

    class Meta:
        model = User


admin.site.register(Abonnement)
admin.site.register(Article)
admin.site.register(User, UserAdmin)
