# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apipoll', '0002_auto_20141213_0548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='post_id',
            field=models.BigIntegerField(unique=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='post_id',
            field=models.BigIntegerField(unique=True),
            preserve_default=True,
        ),
    ]
