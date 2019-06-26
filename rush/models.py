from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone

from users.models import Profile
# Choices

typesofmentions = (
    (1, "Positive"),
    (2, "Negative")
)

gpas = (
    (1, "This is my first semester."),
    (2, "Less Than 2.0"),
    (3, "Between 2.0 and 2.5"),
    (4, "Between 2.5 and 2.75"),
    (5, "Between 2.75 and 3.0"),
    (6, "Between 3.0 and 3.25"),
    (7, "Between 3.25 and 3.5"),
    (8, "Between 3.5 and 3.75"),
    (9, "Above 3.75"),
)

scores = {
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
}

essaytopicchoices = (
    (1, "What is something you are passionate about?"),
    (2, "Talk about a time you failed and how you responded."),
    (3, "When is a time you had to be a leader?"),
    (4, "Talk about a time you had to go above and beyond?"),
	(5, "What specific ways can you contribute to Alpha Kappa Psi?"),
)

votechoices = (
    (1, "Yes"),
    (2, "No"),
    (3, "Abstain")

)

def validate_not_negative(value):
    if value < 0:
        raise ValidationError(
            _('%(values)s is not 0 or higher'),
            params={'value': value},
        )

# Create your models here.

class RushNight(models.Model):
    night = models.IntegerField(default=1, unique=True, blank=False, validators=[validate_not_negative])
    name = models.CharField(max_length=50)
    date = models.DateField()
    interviews = models.BooleanField(default=0)
    voting = models.BooleanField(default=0)
    comment = models.CharField(max_length=120, blank=True)

    def __str__(self):
        return str(self.night) + ': ' + self.name

class RusheeSignin(models.Model):
    rushee = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'profile.isbrother': False})
    night = models.ForeignKey(RushNight, on_delete=models.CASCADE)

    def __str__(self):
        return self.night.name + ': ' + self.rushee.username

    class Meta:
        unique_together = ('rushee', 'night')

class Interview(models.Model):
    rushee = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'profile.isbrother': False}, related_name='interviewgiven')
    interviewer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'profile.isbrother': True})
    interest = models.IntegerField(choices=scores)
    energy = models.IntegerField(choices=scores)
    friendliness = models.IntegerField(choices=scores)
    comment = models.CharField(max_length=200, verbose_name="Negative Comments Only", blank=True)

    def __str__(self):
        return self.interviewer.get_full_name() + " interviewed " + self.rushee.get_full_name()

    class Meta:
        unique_together = ('interviewer', 'rushee')

class Application(models.Model):
    rushee = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'profile.isbrother': False})
    FRESHMAN = 'FR'
    SOPHOMORE = 'SO'
    JUNIOR = 'JR'
    SENIOR = 'SR'
    YEAR_IN_SCHOOL_CHOICES = [
        (FRESHMAN, 'Freshman'),
        (SOPHOMORE, 'Sophomore'),
        (JUNIOR, 'Junior'),
        (SENIOR, 'Senior'),
    ]
    year_in_school = models.CharField(
        max_length=2,
        choices=YEAR_IN_SCHOOL_CHOICES,
        default=FRESHMAN,
    )
    address = models.CharField(max_length=200, verbose_name="School Address")
    cellphone = models.CharField(max_length=30, verbose_name="Cell Phone Number")
    gpa = models.IntegerField(choices=gpas, verbose_name="College GPA*", default=1)
    involvement = models.CharField(max_length=300, verbose_name="What are you involved with on campus?*", null=True, blank=True)
    WhyAKPsi = models.CharField(max_length=500, verbose_name="Why do you want to be part of AKPsi?*", null=True)
    HowDidYouHear = models.CharField(max_length=200, verbose_name="How did you hear about AKPsi?", null=True, blank=True)
    excuses = models.CharField(max_length=200, verbose_name="Do you have any conflicts with any nights of rush? If so what are they? If not leave blank*", null=True, blank=True)
    aboutme = models.CharField(max_length=400, verbose_name='Please use the space below to write an \'About Me\'*', null=True, blank=True)
    essaytopic = models.IntegerField(choices=essaytopicchoices, null=True, verbose_name="Choose an Essay Topic Below!", blank=True)
    essay = models.CharField(max_length=3500, verbose_name="Use The Space Below to Write a Short (less than 500 words) Essay About Your Selected Topic!*", null=True, blank=True)

    def __str__(self):
        return "Application of " + str(self.rushee)

class Mention(models.Model):
    brother = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'profile.isbrother': True}, related_name='mentiongiven')
    rushee = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'profile.isbrother': False})
    night = models.ForeignKey(RushNight, on_delete=models.CASCADE)
    mentiontype = models.IntegerField(choices=typesofmentions, verbose_name="Type of Mention", blank=False, default=1)
    comment = models.CharField(max_length=200, verbose_name="Comment", null=True)

    class Meta:
        unique_together = ('brother', 'rushee')
        ordering = ('night', 'rushee', 'brother')

    def __str__(self):
        return self.night.name + ": " \
               + self.brother.get_full_name() \
               + " made a " + self.get_mentiontype_display() \
               + " mention of " + self.rushee.get_full_name()

class Vote(models.Model):
    brother = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'profile.isbrother': True}, related_name='+')
    rushee = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'profile.isbrother': False})
    choice = models.IntegerField(choices=votechoices, default=3)

    class Meta:
        unique_together = ('brother', 'rushee')

    def __str__(self):
        return str(self.choice)