# --encoding:utf-8


class AjaxMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.is_ajax():
            return self.ajax(request, *args, **kwargs)
        return super(AjaxMixin, self).dispatch(request, *args, **kwargs)
