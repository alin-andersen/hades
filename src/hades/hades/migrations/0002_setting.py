# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('hades', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('animation_in', models.CharField(max_length=128)),
                ('timespan_in', models.PositiveIntegerField(default=0)),
                ('animation_out', models.CharField(max_length=128)),
                ('timespan_out', models.PositiveIntegerField(default=0)),
                ('background_color', models.CharField(max_length=128)),
            ],
        ),
    ]
