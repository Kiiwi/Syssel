# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django import forms

from django.forms.widgets import HiddenInput
from haystack.forms import SearchForm

from .models import User


class UserForm(forms.ModelForm):
    """
    For for updating user information
    """
    def __init__(self, *args, **kwargs):
        """
        Overridden init method to manipulate form fields
        depending in user role
        :param args:
        :param kwargs:
        :return: Hidden and excluded fields
        """
        # Call constructor to set up the fields so they can be modified
        super(UserForm, self).__init__(*args, **kwargs)

        # Exclude student fields
        if self.instance.is_corporate:
            del self.fields["skills"]
            del self.fields["name"]

        # Exclude corporate fields
        if self.instance.is_student:
            del self.fields["corporation"]
            del self.fields["division"]

        # Hide completed field
        self.fields["completed"].widget = HiddenInput()

    # Make fields not required
    completed = forms.CharField(max_length=9, required=False)
    website = forms.CharField(max_length=255, required=False)

    class Meta:
        """
        Setting model form to use User as model
        """
        model = User

        fields = ("name", "website", "corporation",
                  "division", "skills", "description", "completed",)


class SignupForm(forms.Form):
    """
    Form for user signup
    """
    ROLE_CHOICES = (
        ("student", "Student"),
        ("corporate", "Corporate"),
    )
    role = forms.TypedChoiceField(choices=ROLE_CHOICES)

    def signup(self, request, user):
        """
        Method to set user role and save form data
        :param request: GET request
        :param user: User signing up
        :return: Valid form data
        """
        user.role = self.cleaned_data["role"]
        user.save()


class UserSearchForm(SearchForm):
    """
    Form for searching for users
    """
    def search(self):
        """
        Overridden search method to set SQS
        :return:
        """
        sqs = super(UserSearchForm, self).search()

        if not self.is_valid():
            return self.no_query_found()
        return sqs