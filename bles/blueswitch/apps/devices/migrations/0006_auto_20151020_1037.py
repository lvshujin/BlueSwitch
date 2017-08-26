# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0005_auto_20151005_0631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='paired_devices',
            field=models.ManyToManyField(related_name='paired_devices_rel_+', to='devices.Device'),
        ),
    ]
