# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0006_auto_20151020_1037'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='paired_devices',
        ),
        migrations.RemoveField(
            model_name='twindevice',
            name='device1',
        ),
        migrations.RemoveField(
            model_name='twindevice',
            name='device2',
        ),
        migrations.AddField(
            model_name='twindevice',
            name='mac1',
            field=models.CharField(max_length=255, verbose_name='mac address1', default='6C EC EB 57 36 45'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='twindevice',
            name='mac2',
            field=models.CharField(max_length=255, verbose_name='mac address2', default='78 A5 04 07 79 84'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='twindevice',
            name='color',
            field=models.CharField(max_length=25, choices=[('yellow', 'Yellow'), ('magenta', 'Magenta'), ('cyan', 'Cyan'), ('red', 'Red'), ('green', 'Green'), ('blue', 'Blue'), ('white', 'White'), ('black', 'Black'), ('orange', 'Orange'), ('pink', 'Pink')], verbose_name='color', default='red'),
            preserve_default=False,
        ),
    ]
