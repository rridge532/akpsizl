from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Profile, EventGroup, Event, Signin

# Register your models here.

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class EventInline(admin.TabularInline):
    model = Event
    extra = 0
    exclude = ['slug']
    ordering = ['-date']

class SigninInline(admin.TabularInline):
    model = Signin
    extra = 0
    exclude = ['comment']
    classes = ['collapse']

class CustomUserAdmin(UserAdmin):
    inlines = [ProfileInline]

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

class EventGroupAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name']}),
        ('Required Credits', {'fields': ['needed_credits', 'senior_credits'], 'classes': ['collapse']}),
    ]
    inlines = [EventInline]
    list_display = [field.name for field in EventGroup._meta.fields if field.name != 'id']
    ordering = ['name']
    actions = None

class EventAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Event._meta.fields if field.name not in ['id', 'slug']]
    ordering = ['-date', 'group', 'name']
    list_filter = ['group']
    readonly_fields = ['slug']
    search_fields = ['name']
    inlines = [SigninInline]

class SigninAdmin(admin.ModelAdmin):
    list_display = ['event', 'user', 'time']
    ordering = ['-time', 'event', 'user']
    list_filter = ['event','user']

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(EventGroup, EventGroupAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Signin, SigninAdmin)