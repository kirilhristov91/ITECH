# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Guess_The_Movie', '0005_auto_20160312_1321'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movie',
            old_name='poster_ulr',
            new_name='poster_url',
        ),
    ]
