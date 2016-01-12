# flake8: noqa
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
            name='ActionPlanResponse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('action_plan', models.CharField(default=b'', max_length=256)),
                ('assessment', models.TextField(default=b'', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Lab',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField(blank=True)),
                ('assessment', models.BooleanField(default=False)),
                ('sickvisit', models.BooleanField(default=False)),
                ('correct_actionplan', models.CharField(default=b'', max_length=256, choices=[(b'Situation urgent. Call or admit patient immediately', b'Situation urgent. Call or admit patient immediately'), (b'Situation needs follow-up. Call patient within a week', b'Situation needs follow-up. Call patient within a week'), (b'Flag for review at following visit', b'Flag for review at following visit'), (b"Call patient's mother to say the results were normal", b"Call patient's mother to say the results were normal"), (b'Prescribe treatment', b'Prescribe treatment'), (b'Refer for further tests', b'Refer for further tests'), (b'Reassure and send home', b'Reassure and send home')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('ordinality', models.PositiveIntegerField(default=1)),
                ('result', models.CharField(max_length=256)),
                ('normal_range', models.CharField(max_length=256, blank=True)),
                ('unit', models.CharField(max_length=256)),
                ('result_level', models.CharField(default=b'normal', max_length=256, choices=[(b'unselected', b'Please select:'), (b'low', b'Low'), (b'normal', b'Normal'), (b'high', b'High')])),
                ('abnormality', models.CharField(default=b'none', max_length=256)),
                ('lab', models.ForeignKey(to='exercises.Lab')),
            ],
            options={
                'ordering': ('lab', 'ordinality'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TestResponse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('result_level', models.CharField(max_length=256, choices=[(b'unselected', b'Please select:'), (b'low', b'Low'), (b'normal', b'Normal'), (b'high', b'High')])),
                ('abnormality', models.CharField(default=b'none', max_length=256)),
                ('test', models.ForeignKey(to='exercises.Test')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='actionplanresponse',
            name='lab',
            field=models.ForeignKey(to='exercises.Lab'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='actionplanresponse',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
