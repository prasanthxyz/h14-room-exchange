# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=500)),
                ('roomno', models.CharField(max_length=20)),
                ('rollno', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Relationship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('from_person', models.ForeignKey(related_name='from_person', to='room.Person')),
                ('to_person', models.ForeignKey(related_name='to_person', to='room.Person')),
            ],
        ),
    ]
