from django.contrib import admin
from main.models import Article, Package, NewsLetterUser, Subscription, User


class UserAdmin(admin.ModelAdmin):
    search_fields = ['email']
    model = User
    list_display = ['email', 'is_active', 'is_staff', 'is_admin', 'is_superuser']

    fieldsets = (
        (None, {'fields': ('email', )}),
        ('Personal info', {'fields': ['first_name', 'last_name', 'country'
                                      ]}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

class NewsLetterAdmin(admin.ModelAdmin):
    model = NewsLetterUser
    list_display = ['email', 'created_at', 'status']

admin.site.register(Article)
admin.site.register(Package)
admin.site.register(NewsLetterUser, NewsLetterAdmin)
admin.site.register(Subscription)
admin.site.register(User, UserAdmin)
