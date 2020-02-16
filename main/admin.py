from django.contrib import admin
from main.models import Article, Package, Subscription, User


class UserAdmin(admin.ModelAdmin):
    search_fields = ['email']

    class Meta:
        model = User


admin.site.register(Article)
admin.site.register(Package)
admin.site.register(Subscription)
admin.site.register(User, UserAdmin)
