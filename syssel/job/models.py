# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.core.urlresolvers import reverse
from django.db import models

from taggit.managers import TaggableManager

from syssel.users.models import User


class Job(models.Model):
    """
    Job model
    """
    pub_date = models.DateTimeField(auto_now_add=True)
    headline = models.CharField(max_length=255)
    content = models.TextField()
    created_by = models.ForeignKey(User)

    tags = TaggableManager()

    def __unicode__(self):
        return self.headline

    def get_absolute_url(self):
        return reverse('job_detail', kwargs={'headline': self.headline})