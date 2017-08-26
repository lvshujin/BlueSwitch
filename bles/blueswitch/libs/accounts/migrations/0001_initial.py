# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status', default=False)),
                ('email', models.EmailField(unique=True, max_length=255, db_index=True, verbose_name='email address')),
                ('username', models.CharField(unique=True, max_length=255, db_index=True, verbose_name='username')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('profile_picture', models.ImageField(upload_to='profile_picture', null=True, blank=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(help_text='Designates whether the user can log into this admin site.', verbose_name='staff status', default=False)),
                ('is_active', models.BooleanField(help_text='Designates whether this user should be treated as active.  Unselect this instead of deleting accounts.', verbose_name='active', default=True)),
                ('date_joined', models.DateTimeField(verbose_name='date joined', default=django.utils.timezone.now)),
                ('facebook_uid', models.CharField(max_length=32, null=True, blank=True)),
                ('groups', models.ManyToManyField(help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', blank=True, verbose_name='groups', to='auth.Group', related_name='user_set', related_query_name='user')),
                ('paired_users', models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='paired_users_rel_+')),
                ('user_permissions', models.ManyToManyField(help_text='Specific permissions for this user.', blank=True, verbose_name='user permissions', to='auth.Permission', related_name='user_set', related_query_name='user')),
            ],
            options={
                'swappable': 'AUTH_USER_MODEL',
                'verbose_name': 'user',
                'db_table': 'auth_user',
                'verbose_name_plural': 'users',
                'ordering': ['name', 'email'],
            },
        ),
    ]
