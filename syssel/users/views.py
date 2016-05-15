# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin

from braces.views import LoginRequiredMixin

from .forms import UserForm
from .models import User


class UserDetailView(LoginRequiredMixin, DetailView):
    """
    View for user details
    """
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


class UserRedirectView(LoginRequiredMixin, RedirectView):
    """
    View for redirecting users to their profile page
    """
    permanent = False

    def get_redirect_url(self):
        """
        Method to redirect user to their profile page
        :return: URL to user profile with username as keyword argument
        """
        return reverse("users:detail",
                       kwargs={"username": self.request.user.username})


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    View for updating user information
    """
    form_class = UserForm
    model = User
    success_message = "Your profile was successfully updated"

    # send the user back to their own page after a successful update
    def get_success_url(self):
        """
        Method for redirecting user to given URL if form is valid
        :return:
        """
        return reverse("users:detail",
                       kwargs={"username": self.request.user.username})

    def get_object(self):
        """
        Method to only get record for the user making the request
        :return: Record of user making the request
        """
        return User.objects.get(username=self.request.user.username)

    def form_valid(self, form):
        """
        Overridden form_valid to set user.completed if form is valid
        :param form: UserForm
        :return: Saves data from form if valid
        """
        instance = form.save(commit=False)
        instance.completed = "completed"
        return super(UserUpdateView, self).form_valid(form)


class UserListView(LoginRequiredMixin, ListView):
    """
    View for list of users
    """
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = "username"
    slug_url_kwarg = "username"
