# Generated by Django 4.2.4 on 2023-08-30 16:32

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0008_room_profiles'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='profiles',
        ),
        migrations.AddField(
            model_name='room',
            name='participatients',
            field=models.ManyToManyField(related_name='participatients', to=settings.AUTH_USER_MODEL),
        ),
    ]
