# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0004_auto_20150821_0942'),
        ('toggles', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='togglehistory',
            name='devices',
        ),
        migrations.AddField(
            model_name='togglehistory',
            name='devices',
            field=models.ForeignKey(default=1, to='devices.Device'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='toggletransaction',
            name='devices',
        ),
        migrations.AddField(
            model_name='toggletransaction',
            name='devices',
            field=models.ForeignKey(default=1, to='devices.Device'),
            preserve_default=False,
        ),
    ]
