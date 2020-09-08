from django.contrib import admin
from base.admin import admin_site
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User,Group

from .models import Gender, Pronouns, Race, Profile, SignupToken

# Register your models here.

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = [ProfileInline]

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

admin_site.register(Group)
admin_site.register(User, CustomUserAdmin)
admin_site.register(SignupToken)
admin_site.register(Gender)
admin_site.register(Pronouns)
admin_site.register(Race)