# Generated by Django 4.2.4 on 2023-08-30 17:33

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0009_remove_room_profiles_room_participatients'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='participatients',
        ),
        migrations.AddField(
            model_name='room',
            name='participants',
            field=models.ManyToManyField(related_name='participants', to=settings.AUTH_USER_MODEL),
        ),
    ]
