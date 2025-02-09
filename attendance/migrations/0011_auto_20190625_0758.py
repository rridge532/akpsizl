# Generated by Django 2.2.1 on 2019-06-25 12:58

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('attendance', '0010_auto_20190624_2207'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='teammembership',
            options={'verbose_name_plural': 'Team Membership'},
        ),
        migrations.AlterUniqueTogether(
            name='teammembership',
            unique_together={('group', 'user')},
        ),
    ]
