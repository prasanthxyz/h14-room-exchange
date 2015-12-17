# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='phno',
            field=models.CharField(default=b'', max_length=30),
        ),
    ]
