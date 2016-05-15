# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.db import models

from syssel.users.models import User
from syssel.job.models import Job


class Application(models.Model):
    """
    Application model
    """
    applicant = models.ForeignKey(User)
    job_name = models.ForeignKey(Job)
    application_date = models.DateTimeField(auto_now_add=True)