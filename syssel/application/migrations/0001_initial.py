# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('application_date', models.DateTimeField(auto_now_add=True)),
                ('applicant', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('job_name', models.ForeignKey(to='job.Job')),
            ],
        ),
    ]
