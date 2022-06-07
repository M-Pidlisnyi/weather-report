from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from . import models
# Register your models here.


admin.site.register(models.City)

class AppUserInline(admin.StackedInline):
	model = models.AppUser
	can_delete = False
	verbose_name = 'Application user'
	verbose_name_plural = 'Application users'

class UserAdmin(BaseUserAdmin):
	inlines = (AppUserInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
