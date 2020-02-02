from django.db import models
from django.contrib.auth.models import User

from users.models import Profile
# Choices

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

scores = [
    (1, 'Bad (1)'),
    (2, 'Poor (2)'),
    (3, 'Okay (3)'),
    (4, 'Good (4)'),
    (5, 'Great (5)'),
]

essaytopicchoices = (
    (1, "What is something you are passionate about?"),
    (2, "Talk about a time you failed and how you responded."),
    (3, "When is a time you had to be a leader?"),
    (4, "Talk about a time you had to go above and beyond?"),
	(5, "What specific ways can you contribute to Alpha Kappa Psi?"),
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
    interviews = models.BooleanField(default=False)
    voting = models.BooleanField(default=False)
    comment = models.CharField(max_length=120, blank=True)

    def __str__(self):
        return str(self.night) + ': ' + self.name

    class Meta:
        ordering = ['night']

class RusheeSignin(models.Model):
    rushee = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'profile__isbrother': False})
    night = models.ForeignKey(RushNight, on_delete=models.CASCADE)

    def __str__(self):
        return self.night.name + ': ' + self.rushee.username

    class Meta:
        unique_together = ('rushee', 'night')

class Interview(models.Model):
    rushee = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'profile__isbrother': False}, related_name='interviewgiven')
    interviewer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'profile__isbrother': True})
    interest = models.IntegerField(choices=scores)
    energy = models.IntegerField(choices=scores)
    friendliness = models.IntegerField(choices=scores)
    comment = models.CharField(max_length=200, verbose_name="Negative Comments Only", blank=True)

    def __str__(self):
        return self.interviewer.get_full_name() + " interviewed " + self.rushee.get_full_name()

    class Meta:
        unique_together = ('interviewer', 'rushee')

class Application(models.Model):
    rushee = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'profile__isbrother': False})
    address = models.CharField(max_length=200, verbose_name="School Address (Used for bid delivery)")
    cellphone = models.CharField(max_length=30, verbose_name="Cell Phone Number (Used for bid delivery)")
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
        verbose_name="Year*"
    )
    major = models.CharField(max_length=50, verbose_name="Major*", blank=True)
    gpa = models.IntegerField(choices=gpas, verbose_name="College GPA*")
    involvement = models.CharField(max_length=300, verbose_name="What are you involved with on campus?*", blank=True)
    WhyAKPsi = models.CharField(max_length=500, verbose_name="Why do you want to be part of AKPsi?*", blank=True)
    HowDidYouHear = models.CharField(max_length=200, verbose_name="How did you hear about AKPsi?*", blank=True)
    excuses = models.CharField(max_length=200, verbose_name="Any conflicts with any nights of rush? If so, what are they? If not, leave blank*", blank=True)
    aboutme = models.CharField(max_length=400, verbose_name='Please use the space below to write an \'About Me\'*', blank=True)
    essaytopic = models.IntegerField(choices=essaytopicchoices, verbose_name="Essay Topic*", blank=True)
    essay = models.CharField(max_length=3500, verbose_name="Write a Short (less than 500 words) Essay About Your Selected Topic!*", blank=True)

    def __str__(self):
        return "Application of " + str(self.rushee)

class Mention(models.Model):
    brother = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'profile__isbrother': True}, related_name='mentiongiven')
    rushee = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'profile__isbrother': False})
    night = models.ForeignKey(RushNight, on_delete=models.CASCADE)
    POSITIVE = 'P'
    NEGATIVE = 'N'
    TYPES_OF_MENTIONS = [
        (POSITIVE, 'Positive'),
        (NEGATIVE, 'Negative'),
    ]
    mentiontype = models.CharField(
        max_length=1,
        choices=TYPES_OF_MENTIONS,
        verbose_name="Type of Mention",
        blank=False,
        default=POSITIVE,
    )
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
    brother = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'profile__isbrother': True}, related_name='+')
    rushee = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'profile__isbrother': False})
    YES = 'Y'
    NO = 'N'
    ABSTAIN = 'A'
    VOTE_CHOICES = [
        (YES, 'Yes'),        
        (NO, 'No'),        
        (ABSTAIN, 'Abstain'),
    ]
    choice = models.CharField(
        max_length=1,
        choices=VOTE_CHOICES,
        default=ABSTAIN,
    )

    class Meta:
        unique_together = ('brother', 'rushee')

    def __str__(self):
        return str(self.choice)
