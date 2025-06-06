# Generated by Django 4.2.16 on 2025-05-27 00:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('books', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpreference',
            name='avoided_genres',
            field=models.ManyToManyField(blank=True, related_name='avoided_by', to='books.category'),
        ),
        migrations.AddField(
            model_name='userpreference',
            name='avoided_keywords',
            field=models.ManyToManyField(blank=True, to='accounts.avoidedkeyword'),
        ),
        migrations.AddField(
            model_name='userpreference',
            name='interested_genres',
            field=models.ManyToManyField(blank=True, related_name='preferred_by', to='books.category'),
        ),
        migrations.AddField(
            model_name='userpreference',
            name='lifestyles',
            field=models.ManyToManyField(blank=True, to='accounts.lifestylekeyword'),
        ),
        migrations.AddField(
            model_name='userpreference',
            name='preferred_reading_styles',
            field=models.ManyToManyField(blank=True, to='accounts.readingstyle'),
        ),
        migrations.AddField(
            model_name='userpreference',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='preference', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='followings',
            field=models.ManyToManyField(related_name='followers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
