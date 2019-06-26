from django.contrib import admin

from .models import RushNight, RusheeSignin, Interview, Application, Mention, Vote
# Register your models here.

admin.site.register(RushNight)
admin.site.register(RusheeSignin)
admin.site.register(Interview)
admin.site.register(Application)
admin.site.register(Mention)
admin.site.register(Vote)
