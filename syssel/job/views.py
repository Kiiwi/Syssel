# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.shortcuts import render_to_response, RequestContext, render
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import DetailView, ListView, DeleteView, UpdateView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test

from braces.views import LoginRequiredMixin
from haystack.generic_views import SearchView

from .forms import JobForm
from .models import Job

from syssel.contrib.utils import is_corporate, AuthorRequiredMixin


@login_required()
@user_passes_test(is_corporate, redirect_field_name=None)
def job_posting_view(request):
    """
    View for  posting jobs
    :param request: get request
    :return: job posting form
    """
    form = JobForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.created_by = request.user
        instance.save()
        form.save_m2m()

        return HttpResponseRedirect(reverse('users:my_jobs', kwargs={"username": request.user.username}))
    return render_to_response("job/job_posting.html", {
        "form": form,
    }, context_instance=RequestContext(request))


class JobDetailView(LoginRequiredMixin, DetailView):
    """
    View for a detailed view for each job post
    """
    model = Job
    slug_field = "headline"
    slug_url_kwarg = "headline"


class JobUpdateView(AuthorRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    View for updating a job posting
    """
    form_class = JobForm
    model = Job
    success_message = "%(headline)s was successfully updated"

    slug_field = "headline"
    slug_url_kwarg = "headline"

    def get_success_url(self):
        """
        Redirects to given URL if form is valid
        :return: URL with keyword argument for that URL
        """
        return reverse("job:job_detail", kwargs={'headline': self.object.headline})

    def get_success_message(self, cleaned_data):
        """
        Creates a message if update was successful
        :param cleaned_data: Data from form to be used in message
        :return: Message displayed at URL given by success_url
        """
        return self.success_message % dict(cleaned_data, headline=self.object.headline)


class JobListView(ListView):
    """
    View for a list of all posted jobs
    """
    model = Job
    slug_field = "headline"
    slug_url_kwarg = "headline"


class JobDeleteView(AuthorRequiredMixin, DeleteView):
    """
    View for deleting a job post
    """
    model = Job
    success_url = reverse_lazy('job:job_listing')
    success_message = "The job was deleted successfully"

    slug_field = "headline"
    slug_url_kwarg = "headline"

    def delete(self, request, *args, **kwargs):
        """
        Overridden delete method to allow success message
        :param request: GET request
        :param args:
        :param kwargs:
        :return: Deletes job and redirects to success_url
        """
        messages.success(self.request, self.success_message)
        return super(JobDeleteView, self).delete(request, *args, **kwargs)


class MyJobsListView(LoginRequiredMixin, ListView):
    """
    View for list of jobs created by user
    """
    model = Job
    template_name = "job/my_jobs_list.html"
    slug_field = "headline"
    slug_url_kwarg = "headline"

    def get_queryset(self):
        """
        Method to get relevant data from model
        :return: Job posts created by user
        """
        return Job.objects.filter(created_by__username=self.request.user)

