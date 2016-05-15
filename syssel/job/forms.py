# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django import forms

from haystack.forms import SearchForm

from .models import Job


class JobForm(forms.ModelForm):
    """
    Form to create job posts
    """
    class Meta:
        """
        Setting form to use Job as model
        """
        model = Job
        fields = ["headline", "content", "tags",]


class JobSearchForm(SearchForm):
    """
    Form to search for jobs
    """
    def search(self):
        """
        Overridden search method to set SQS
        :return:
        """
        sqs = super(JobSearchForm, self).search()

        if not self.is_valid():
            return self.no_query_found()
        return sqs