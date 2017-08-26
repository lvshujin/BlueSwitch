# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('toggles', '0004_auto_20151217_0726'),
    ]

    operations = [
        migrations.AddField(
            model_name='togglehistory',
            name='address',
            field=models.CharField(max_length=255, default=1, verbose_name='mac address'),
            preserve_default=False,
        ),
    ]
