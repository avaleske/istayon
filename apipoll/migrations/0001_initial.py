# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlogEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('post_datetime', models.DateTimeField()),
                ('liked_datetime', models.DateTimeField()),
                ('post_url', models.URLField()),
                ('post_id', models.BigIntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
