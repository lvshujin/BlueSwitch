# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0002_auto_20150820_0811'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='color',
            field=models.CharField(verbose_name='color', null=True, blank=True, max_length=255),
        ),
    ]
