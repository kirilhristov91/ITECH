# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GameSession',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('points', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('option_a', models.CharField(max_length=256)),
                ('option_b', models.CharField(max_length=256)),
                ('option_c', models.CharField(max_length=256)),
                ('option_d', models.CharField(max_length=256)),
                ('image', models.URLField()),
                ('correct_answer', models.IntegerField(default=0)),
                ('selected', models.IntegerField(default=0)),
                ('game_session_id', models.ForeignKey(to='Guess_The_Movie.GameSession')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('picture', models.ImageField(upload_to=b'profile_images', blank=True)),
                ('game_session_counter', models.IntegerField(default=0)),
                ('total_points', models.IntegerField(default=0)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='gamesession',
            name='user_id',
            field=models.ForeignKey(to='Guess_The_Movie.UserProfile'),
            preserve_default=True,
        ),
    ]
