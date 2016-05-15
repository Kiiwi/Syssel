# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models


class User(AbstractUser):
    """
    User model that extends the AbstractUser model
    """
    # Role field
    role = models.CharField(max_length=255)

    # Common fields
    website = models.URLField(max_length=255)
    description = models.TextField(max_length=1023)
    completed = models.CharField(max_length=9)

    # Corporate fields
    corporation = models.CharField(max_length=255)
    division = models.CharField(max_length=255)

    # Student fields
    name = models.CharField(max_length=255)
    skills = models.TextField(max_length=1023)

    def __unicode__(self):
        return self.username

    @models.permalink
    def get_absolute_url(self):
        """
        Method to get absolute user URLs
        :return: Absolute user URL
        """
        return reverse('users:detail', kwargs={'username': self.username})

    @property
    def is_corporate(self):
        """
        Property method to determine if user has a corporate role
        :return: True if user has a corporate role
        """
        if self.role == "corporate":
            return True
        else:
            return False

    @property
    def is_student(self):
        """
        Property method to determine if user has a student role
        :return: True if user has a student role
        """
        if self.role == "student":
            return True
        else:
            return False

    @property
    def is_complete(self):
        """
        Method to determine if user has completed their profile
        :return: True if user has completed their profile
        """
        if self.completed == "completed":
            return True
        else:
            return False