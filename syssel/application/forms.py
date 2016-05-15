# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django import forms

from syssel.users.models import User
from syssel.job.models import Job
from .models import Application


class ApplicationForm(forms.ModelForm):
    """
    Form to create applications
    """
    applicant = forms.ModelChoiceField(queryset=User.objects.all(), required=False)
    job_name = forms.ModelChoiceField(queryset=Job.objects.all(), required=False)

    class Meta:
        """
        Setting form to use Application as model
        """
        model = Application
        fields = ["applicant", "job_name",]