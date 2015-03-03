# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('salary', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='survey',
            old_name='tracker',
            new_name='_tracker',
        ),
    ]
