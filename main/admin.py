from .models import User
from django.contrib import admin

class UserAdmin(admin.ModelAdmin):
	search_fields = ['email']
	class Meta:
		Model = User 

admin.site.register(User, UserAdmin)
