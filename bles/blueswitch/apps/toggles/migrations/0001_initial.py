# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ToggleHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('devices', models.ManyToManyField(to='devices.Device')),
            ],
        ),
        migrations.CreateModel(
            name='ToggleTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('status', models.CharField(max_length=10, choices=[('pending', 'Pending'), ('success', 'Success'), ('failed', 'Failed')])),
                ('transaction_at', models.DateTimeField(auto_now=True)),
                ('devices', models.ManyToManyField(to='devices.Device')),
            ],
        ),
    ]
