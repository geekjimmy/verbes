# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-10 03:37
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('verbes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserMoodTense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mood_tense', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='verbes.MoodTense')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='moodtense',
            name='users',
            field=models.ManyToManyField(through='verbes.UserMoodTense', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='usermoodtense',
            unique_together=set([('user', 'mood_tense')]),
        ),
    ]
