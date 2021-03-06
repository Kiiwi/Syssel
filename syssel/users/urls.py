# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from syssel.job.views import MyJobsListView
from syssel.application.views import MyApplicationsListView

from haystack.views import SearchView
from haystack.query import SearchQuerySet

from . import views

from syssel.users.forms import UserSearchForm

urlpatterns = [
    # URL pattern for the UserListView
    url(
        regex=r'^$',
        view=views.UserListView.as_view(),
        name='list'
    ),

    # URL patter for search
    url(r'^search/$', SearchView(
        template='users/user_search.html',
        searchqueryset=SearchQuerySet().filter(),
        form_class=UserSearchForm
        ), name="user_search"),

    # URL pattern for the UserRedirectView
    url(
        regex=r'^~redirect/$',
        view=views.UserRedirectView.as_view(),
        name='redirect'
    ),

    # URL pattern for the UserDetailView
    url(
        regex=r'^(?P<username>[\w.@+-]+)/$',
        view=views.UserDetailView.as_view(),
        name='detail'
    ),

    # URL pattern for the UserUpdateView
    url(
        regex=r'^~update/$',
        view=views.UserUpdateView.as_view(),
        name='update'
    ),

    # URL pattern for the MyJobsListView
    url(
        regex=r'^(?P<username>[\w.@+-]+)/myjobs/$',
        view=MyJobsListView.as_view(),
        name='my_jobs'
    ),

    # URL pattern for the MyApplicationsListView
    url(
        regex=r'^(?P<username>[\w.@+-]+)/myapplications/$',
        view=MyApplicationsListView.as_view(),
        name='my_applications'
    ),
]
