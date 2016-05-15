from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


def is_corporate(user):
    """
    Method to determine if user has a corporate role
    :param user: User making the request
    :return: True if user has a corporate role
    """
    return user.role == "corporate"


def is_student(user):
    """
    Method to determine if user has a student role
    :param user: User making the request
    :return: True if user has a student role
    """
    return user.role == "student"


class AuthorRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.created_by != self.request.user:
            return HttpResponseRedirect(reverse('job_listing'))
        return super(AuthorRequiredMixin, self).dispatch(request, *args, **kwargs)