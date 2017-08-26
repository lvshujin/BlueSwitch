# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0003_auto_20150821_0658'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='twindevice',
            name='paired_devices',
        ),
        migrations.AddField(
            model_name='device',
            name='paired_devices',
            field=models.ManyToManyField(to='devices.Device', related_name='paired_devices_rel_+'),
        ),
        migrations.AddField(
            model_name='twindevice',
            name='color',
            field=models.CharField(verbose_name='color', max_length=255, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='twindevice',
            name='device1',
            field=models.ForeignKey(to='devices.Device', default=1, related_name='first_device'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='twindevice',
            name='device2',
            field=models.ForeignKey(to='devices.Device', default=2, related_name='second_device'),
            preserve_default=False,
        ),
    ]
