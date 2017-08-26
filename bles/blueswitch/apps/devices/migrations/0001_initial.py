# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='device name')),
                ('color', models.CharField(max_length=255, verbose_name='color')),
                ('address', models.CharField(unique=True, max_length=255, verbose_name='mac address')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='users')),
            ],
        ),
        migrations.CreateModel(
            name='TwinDevice',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('paired_at', models.DateTimeField(auto_now=True)),
                ('paired_devices', models.ManyToManyField(to='devices.Device')),
            ],
        ),
    ]
