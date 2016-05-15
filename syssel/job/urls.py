# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from haystack.views import SearchView
from haystack.query import SearchQuerySet

from syssel.application.views import apply_view, ApplicationListView, ApplicationDeleteView

from . import views

from syssel.job.forms import JobSearchForm

urlpatterns = [
    # URL pattern for the JobListView
    url(
        regex=r'^$',
        view=views.JobListView.as_view(),
        name='job_listing'
    ),

    # URL pattern for job search
    url(r'^search/$', SearchView(
        template='job/job_search.html',
        searchqueryset=SearchQuerySet().filter(),
        form_class=JobSearchForm
        ), name="job_search"),

    # URL pattern for the job_posting_view
    url(
        regex=r'^post/$',
        view=views.job_posting_view,
        name='job_posting'
    ),

    # URL pattern for the JobDetailView
    url(
        regex=r'^(?P<headline>[\w.@+-]+)/$',
        view=views.JobDetailView.as_view(),
        name='job_detail'
    ),

    # URL pattern for the JobUpdateView
    url(
        regex=r'^(?P<headline>[\w.@+-]+)/update/$',
        view=views.JobUpdateView.as_view(),
        name='job_update'
    ),

    # URL pattern for the JobDeleteView
    url(
        regex=r'^(?P<headline>[\w.@+-]+)/delete/$',
        view=views.JobDeleteView.as_view(),
        name='job_delete'
    ),

    # URL pattern for the UserListView
    url(
        regex=r'^(?P<headline>[\w.@+-]+)/apply/$',
        view=apply_view,
        name='apply'
    ),

    # URL pattern for the ApplicationsListView
    url(
        regex=r'^(?P<job>[\w.@+-]+)/applications/$',
        view=ApplicationListView.as_view(),
        name='application_listing'
    ),

    # URL pattern for the ApplicationsDeleteView
    url(
        regex=r'^(?P<job>[\w.@+-]+)/applications/delete/$',
        view=ApplicationDeleteView.as_view(),
        name='application_delete'
    ),
]
