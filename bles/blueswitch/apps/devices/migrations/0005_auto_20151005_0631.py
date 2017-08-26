# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0004_auto_20150821_0942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='paired_devices',
            field=models.ManyToManyField(null=True, related_name='paired_devices_rel_+', to='devices.Device', blank=True),
        ),
    ]
