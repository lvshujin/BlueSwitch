# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('toggles', '0003_auto_20150821_1022'),
    ]

    operations = [
        migrations.RenameField(
            model_name='togglehistory',
            old_name='created_at',
            new_name='toggled_at',
        ),
        migrations.RemoveField(
            model_name='togglehistory',
            name='device',
        ),
        migrations.AddField(
            model_name='togglehistory',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, default=1, related_name='toggle_historys'),
            preserve_default=False,
        ),
    ]
