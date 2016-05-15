# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.shortcuts import render_to_response, RequestContext
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import ListView, DeleteView

from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q

from braces.views import LoginRequiredMixin

from .forms import ApplicationForm
from .models import Application
from syssel.contrib.utils import is_student
from syssel.job.models import Job


@login_required()
@user_passes_test(is_student, redirect_field_name=None)
def apply_view(request, **kwargs):
    """
    View for creating application
    :param request: GET request
    :param kwargs:
    :return: Application form with redirect if valid
    """
    form = ApplicationForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.applicant = request.user
        job = Job.objects.filter(headline=kwargs['headline'])[0]
        instance.job_name = job
        instance.save()

        return HttpResponseRedirect(reverse('users:my_applications', kwargs={"username": request.user.username}))
    return render_to_response("application/application_form.html", {
        "form": form,
    }, context_instance=RequestContext(request))


class MyApplicationsListView(LoginRequiredMixin, ListView):
    """
    View for a list of applications created by user
    """
    model = Application
    template_name = "application/my_applications_list.html"
    slug_field = "headline"
    slug_url_kwarg = "headline"

    #@user_passes_test(is_student, redirect_field_name=None)
    def dispatch(self, *args, **kwargs):
        """
        Overridden dispatch method to apply decorator to CBV
        :param args:
        :param kwargs:
        :return: MyApplication view with decorator
        """
        return super(MyApplicationsListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        """
        Method to get relevant data
        :return: Applications created by user
        """
        return Application.objects.filter(applicant__username=self.request.user)


class ApplicationListView(LoginRequiredMixin, ListView):
    """
    View for list over applications made to users job posting
    """
    model = Application

    def get_context_data(self, **kwargs):
        context = super(ApplicationListView, self).get_context_data(**kwargs)
        context['headline'] = self.kwargs['job']
        return context

    def get_queryset(self):
        """
        Method to get relevant data
        :return: Applications for jobs that are created by user AND has headline
        matching keyword argument given in URL
        """
        return Application.objects.filter(
            Q(job_name__headline=self.kwargs['job']) & Q(job_name__created_by=self.request.user))


class ApplicationDeleteView(LoginRequiredMixin, DeleteView):
    """
    View for deleting an application
    """
    model = Application
    success_url = reverse_lazy('job:application_delete')
    success_message = "The application was deleted successfully"

    slug_field = "applicant"
    slug_url_kwarg = "applicant"

    def delete(self, request, *args, **kwargs):
        """
        Overridden delete method to allow success message
        :param request: GET request
        :param args:
        :param kwargs:
        :return: Deletes job and redirects to success_url
        """
        messages.success(self.request, self.success_message)
        return super(ApplicationDeleteView, self).delete(request, *args, **kwargs)