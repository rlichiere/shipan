# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator


class SuperuserRequiredMixin(object):  # only superuser can access views
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(SuperuserRequiredMixin, self).dispatch(*args, **kwargs)
