from django.contrib import admin
from base import filters
from .models import EventGroup, Event, Signin, TeamMembership

# Register your models here.

class EventInline(admin.TabularInline):
    exclude = ['slug']
    extra = 0
    model = Event
    ordering = ['-date']

class SigninInline(admin.TabularInline):
    autocomplete_fields = ['user']
    classes = ['collapse']
    exclude = ['comment']
    extra = 1
    model = Signin
    verbose_name = 'sign-in'
    verbose_name_plural = 'New sign-in'

    def has_change_permission(self, request, obj=None):
        return False
    
    def has_view_permission(self, request, obj=None):
        return False

class EventGroupAdmin(admin.ModelAdmin):
    actions = None
    fieldsets = [
        (None, {
            'fields': ['name']
        }),
        ('Required Credits', {
            'fields': ['needed_credits', 'senior_credits'],
            'classes': ['collapse']
        }),
    ]
    inlines = [EventInline]
    list_display = [field.name for field in EventGroup._meta.fields if field.name != 'id']
    list_editable = [field.name for field in EventGroup._meta.fields if field.name not in ['id','name']]
    ordering = ['name']
    search_fields = ['name']

class EventAdmin(admin.ModelAdmin):
    autocomplete_fields = ['group']
    date_hierarchy = 'date'
    inlines = [SigninInline]
    list_display = [field.name for field in Event._meta.fields if field.name not in ['id', 'slug']]
    list_filter = ['group']
    ordering = ['-date', 'group', 'name']
    readonly_fields = ['slug']
    search_fields = ['name']

class SigninAdmin(admin.ModelAdmin):
    autocomplete_fields = ['event','user']
    date_hierarchy = 'signintime'
    list_display = ['user','event','signintime','signouttime','attendance_duration']
    list_filter = [
        ('event',filters.RelatedDropdownFilter),
        ('user',filters.RelatedDropdownFilter),
        ('event__group',filters.RelatedDropdownFilter),
    ]
    list_per_page = 50
    ordering = ['-signintime', 'event', 'user']
    readonly_fields = ['attendance_duration']
    search_fields = ['event__name','user__username','user__first_name','user__last_name']

admin.site.register(EventGroup, EventGroupAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Signin, SigninAdmin)
admin.site.register(TeamMembership)