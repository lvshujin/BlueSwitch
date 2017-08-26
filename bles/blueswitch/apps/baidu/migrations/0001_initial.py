# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import blueswitch.apps.baidu.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BaiduDevice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(blank=True, verbose_name='Name', null=True, max_length=255)),
                ('active', models.BooleanField(verbose_name='Is active', help_text='Inactive devices will not be sent notifications', default=True)),
                ('date_created', models.DateTimeField(verbose_name='Creation date', null=True, auto_now_add=True)),
                ('device_id', blueswitch.apps.baidu.fields.HexIntegerField(blank=True, verbose_name='Device ID', help_text='android device id (always as hex)', null=True, db_index=True)),
                ('buser_id', models.TextField(verbose_name='Baidu User ID')),
                ('bchannel_id', models.TextField(verbose_name='Baidu Channel ID')),
                ('user', models.ForeignKey(blank=True, null=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Baidu device',
            },
        ),
    ]
