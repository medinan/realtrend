from django.shortcuts import render
from django.views import generic
from api.utils import AuthMercadoLibreMixin, handler_app
from django.db import transaction
from products import models as pro_models
from products import forms as prod_forms
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from api.utils import AjaxMixin
from django.db.models import Q
from django.template.loader import render_to_string
from django.http import JsonResponse
# Create your views here.


class IngresoTemplateView(AuthMercadoLibreMixin, generic.TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        data = super(IngresoTemplateView, self).get_context_data(**kwargs)
        data['url_login'] = self.url_login
        return data


class AutorizacionTemplateView(AuthMercadoLibreMixin, generic.TemplateView):
    template_name = 'index.html'

    def get(self):
        handler_app.authorize(self.request.GET.get('code'), self.url_redirect)
        self.request.session['token'] = handler_app.access_token
        redirect(reverse('ingreso'))

    def get_context_data(self, **kwargs):
        data = super(IngresoTemplateView, self).get_context_data(**kwargs)
        data['url_login'] = self.url_login
        return data
