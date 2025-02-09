# Generated by Django 2.2.1 on 2019-07-01 05:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rush', '0004_auto_20190625_2144'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='major',
            field=models.CharField(blank=True, max_length=50, verbose_name='Major*'),
        ),
        migrations.AlterField(
            model_name='application',
            name='HowDidYouHear',
            field=models.CharField(blank=True, default='sdlkfjsd', max_length=200, verbose_name='How did you hear about AKPsi?*'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='application',
            name='WhyAKPsi',
            field=models.CharField(blank=True, default='aslkfjdf', max_length=500, verbose_name='Why do you want to be part of AKPsi?*'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='application',
            name='aboutme',
            field=models.CharField(blank=True, default='asdlfkja', max_length=400, verbose_name="Please use the space below to write an 'About Me'*"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='application',
            name='essay',
            field=models.CharField(blank=True, default='', max_length=3500, verbose_name='Use The Space Below to Write a Short (less than 500 words) Essay About Your Selected Topic!*'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='application',
            name='essaytopic',
            field=models.IntegerField(blank=True, choices=[(1, 'What is something you are passionate about?'), (2, 'Talk about a time you failed and how you responded.'), (3, 'When is a time you had to be a leader?'), (4, 'Talk about a time you had to go above and beyond?'), (5, 'What specific ways can you contribute to Alpha Kappa Psi?')], default=1, verbose_name='Choose an Essay Topic Below!*'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='application',
            name='excuses',
            field=models.CharField(blank=True, default='', max_length=200, verbose_name='Do you have any conflicts with any nights of rush? If so what are they? If not leave blank*'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='application',
            name='gpa',
            field=models.IntegerField(choices=[(1, 'This is my first semester.'), (2, 'Less Than 2.0'), (3, 'Between 2.0 and 2.5'), (4, 'Between 2.5 and 2.75'), (5, 'Between 2.75 and 3.0'), (6, 'Between 3.0 and 3.25'), (7, 'Between 3.25 and 3.5'), (8, 'Between 3.5 and 3.75'), (9, 'Above 3.75')], verbose_name='College GPA*'),
        ),
        migrations.AlterField(
            model_name='application',
            name='involvement',
            field=models.CharField(blank=True, default='asdlfj', max_length=300, verbose_name='What are you involved with on campus?*'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='application',
            name='rushee',
            field=models.ForeignKey(limit_choices_to={'profile__isbrother': False}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='interview',
            name='energy',
            field=models.IntegerField(choices=[(1, 'Bad (1)'), (2, 'Poor (2)'), (3, 'Okay (3)'), (4, 'Good (4)'), (5, 'Great (5)')]),
        ),
        migrations.AlterField(
            model_name='interview',
            name='friendliness',
            field=models.IntegerField(choices=[(1, 'Bad (1)'), (2, 'Poor (2)'), (3, 'Okay (3)'), (4, 'Good (4)'), (5, 'Great (5)')]),
        ),
        migrations.AlterField(
            model_name='interview',
            name='interest',
            field=models.IntegerField(choices=[(1, 'Bad (1)'), (2, 'Poor (2)'), (3, 'Okay (3)'), (4, 'Good (4)'), (5, 'Great (5)')]),
        ),
        migrations.AlterField(
            model_name='interview',
            name='interviewer',
            field=models.ForeignKey(limit_choices_to={'profile__isbrother': True}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='interview',
            name='rushee',
            field=models.ForeignKey(limit_choices_to={'profile__isbrother': False}, on_delete=django.db.models.deletion.CASCADE, related_name='interviewgiven', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='mention',
            name='brother',
            field=models.ForeignKey(limit_choices_to={'profile__isbrother': True}, on_delete=django.db.models.deletion.CASCADE, related_name='mentiongiven', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='mention',
            name='rushee',
            field=models.ForeignKey(limit_choices_to={'profile__isbrother': False}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='rusheesignin',
            name='rushee',
            field=models.ForeignKey(limit_choices_to={'profile__isbrother': False}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='vote',
            name='brother',
            field=models.ForeignKey(limit_choices_to={'profile__isbrother': True}, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='vote',
            name='rushee',
            field=models.ForeignKey(limit_choices_to={'profile__isbrother': False}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
