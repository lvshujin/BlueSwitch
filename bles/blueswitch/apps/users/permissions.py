from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test, login_required

from rest_framework import permissions


class AdminPermissionMixin(View):
    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: u.is_admin))
    def dispatch(self, *args, **kwargs):
        return super(AdminPermissionMixin, self).dispatch(*args, **kwargs)
