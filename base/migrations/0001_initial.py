# Generated by Django 4.2.4 on 2023-08-25 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TimeField()),
                ('email', models.EmailField(max_length=254, verbose_name='email')),
                ('about', models.TextField(blank=True, null=True, verbose_name='about')),
            ],
        ),
    ]
