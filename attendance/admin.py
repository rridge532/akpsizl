from django.contrib import admin

from .models import EventGroup, Event, Signin, TeamMembership

# Register your models here.

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

admin.site.register(EventGroup, EventGroupAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Signin, SigninAdmin)
admin.site.register(TeamMembership)