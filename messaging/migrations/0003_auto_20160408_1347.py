# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0002_message_sent_by_me'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='time_stamp',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
