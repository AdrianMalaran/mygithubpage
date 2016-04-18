# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=20, null=True, blank=True)),
                ('last_name', models.CharField(max_length=20, null=True, blank=True)),
                ('phone_number', models.CharField(max_length=15, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('time_stamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('contact', models.ForeignKey(related_name='messages', blank=True, to='messaging.Contact', null=True)),
            ],
        ),
    ]
