# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import disparity.apps.salary.models
import uuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', uuidfield.fields.UUIDField(unique=True, max_length=32, editable=False, blank=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('total', models.BigIntegerField(default=disparity.apps.salary.models.get_default_total)),
                ('tracker', models.CharField(default=b'1', max_length=10000, null=True)),
                ('num_collected', models.PositiveIntegerField(default=0, null=True)),
                ('num_expected', models.PositiveIntegerField(null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
