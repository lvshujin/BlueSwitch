# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('toggles', '0002_auto_20150821_1008'),
    ]

    operations = [
        migrations.RenameField(
            model_name='togglehistory',
            old_name='devices',
            new_name='device',
        ),
        migrations.RenameField(
            model_name='toggletransaction',
            old_name='devices',
            new_name='device',
        ),
    ]
