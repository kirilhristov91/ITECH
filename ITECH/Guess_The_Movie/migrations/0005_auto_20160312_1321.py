# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Guess_The_Movie', '0004_auto_20160227_1610'),
    ]

    operations = [
        migrations.CreateModel(
            name='Favourites',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('imdb_id', models.CharField(max_length=9)),
                ('title', models.CharField(max_length=256)),
                ('image_url', models.URLField()),
                ('poster_ulr', models.URLField()),
                ('other_options', models.CharField(max_length=1024)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='favourites',
            name='movie',
            field=models.ForeignKey(to='Guess_The_Movie.Movie'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='favourites',
            name='user',
            field=models.ForeignKey(to='Guess_The_Movie.UserProfile'),
            preserve_default=True,
        ),
        migrations.RenameField(
            model_name='gamesession',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='game_session_id',
            new_name='game_session',
        ),
        migrations.RemoveField(
            model_name='question',
            name='correct_answer',
        ),
        migrations.RemoveField(
            model_name='question',
            name='image',
        ),
        migrations.RemoveField(
            model_name='question',
            name='option_a',
        ),
        migrations.RemoveField(
            model_name='question',
            name='option_b',
        ),
        migrations.RemoveField(
            model_name='question',
            name='option_c',
        ),
        migrations.RemoveField(
            model_name='question',
            name='option_d',
        ),
        migrations.RemoveField(
            model_name='question',
            name='selected',
        ),
        migrations.AddField(
            model_name='question',
            name='is_guess_correct',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='question',
            name='movie',
            field=models.ForeignKey(default='', to='Guess_The_Movie.Movie'),
            preserve_default=False,
        ),
    ]
