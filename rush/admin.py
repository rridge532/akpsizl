from django.contrib import admin
from base import filters
from .models import RushNight, RusheeSignin, Interview, Application, Mention, Vote
# Register your models here.

# class RusheeSigninInline(admin.TabularInline):
#     extra = 0
#     model = RusheeSignin

# class InterviewInline(admin.TabularInline):
#     extra = 0
#     model = Interview
#     fk_name = 'rushee'

# class MentionInline(admin.TabularInline):
#     extra = 0
#     model = Mention
#     fk_name = 'rushee'

# class VoteInline(admin.TabularInline):
#     extra = 0
#     model = Vote
#     fk_name = 'rushee'

#     def get_queryset(self, request):
#         qs = Vote.objects.filter(rushee=request.rushee)
#         return qs

class ApplicationAdmin(admin.ModelAdmin):
    autocomplete_fields = ['rushee']
    # inlines = [InterviewInline,MentionInline,VoteInline]
    list_display = ['rushee','year_in_school','get_votes','get_mentions','get_attendance']
    list_filter = [
        ('rushee__rusheesignin__night',filters.RelatedDropdownFilter),
    ]
    search_fields = ['rushee__first_name', 'rushee__last_name', 'rushee__username']
    radio_fields = { 'year_in_school': admin.HORIZONTAL }
    readonly_fields = ['get_votes','get_mentions','get_attendance']

    # def get_inline_instances(self, request, obj=None):
    #     if not obj:
    #         return list()
    #     return super(ApplicationAdmin, self).get_inline_instances(request, obj.rushee)

    def get_votes(self, obj=None):
        votes = Vote.objects.filter(rushee=obj.rushee).all()
        total = votes.count()
        yes = votes.filter(choice='Y').count()
        no = votes.filter(choice='N').count()
        abstain = votes.filter(choice='A').count()
        return "Yes: %s; No: %s; Abstain: %s; Total: %s" % (yes, no, abstain,total)
    get_votes.short_description = 'Votes'

    def get_mentions(self, obj=None):
        mentions = Mention.objects.filter(rushee=obj.rushee).all()
        total = mentions.count()
        positive = mentions.filter(mentiontype='P').count()
        negative = mentions.filter(mentiontype='N').count()
        return "Positive: %s; Negative: %s; Total: %s" % (positive, negative, total)
    get_mentions.short_description = 'Mentions'

    def get_attendance(self, obj=None):
        signins = RusheeSignin.objects.filter(rushee=obj.rushee).all()
        total = signins.count()
        nights = [signin.night.night for signin in signins]
        nights.sort()
        return nights
    get_attendance.short_description = 'Nights Attended'


admin.site.register(RushNight)
admin.site.register(RusheeSignin)
admin.site.register(Interview)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(Mention)
admin.site.register(Vote)
