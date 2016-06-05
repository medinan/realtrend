from django.shortcuts import render
from django.views import generic
from django.conf import settings
from django.db import transaction
from products import models as pro_models
from products import forms as prod_forms
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from api.utils import AuthMercadoLibreMixin
from mercadolibre import query
from api.utils import AjaxMixin
from django.db.models import Q
from django.template.loader import render_to_string
from django.http import JsonResponse
# Create your views here.


class LoginRedirectView(AuthMercadoLibreMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        if self.request.session.get(settings.MERCADO_LIBRE_APP_ACCESS_TOKEN):
            return reverse('home')
        else:
            return self.url_login


class IndexTemplateView(AuthMercadoLibreMixin, generic.TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        data = super(IndexTemplateView, self).get_context_data(**kwargs)
        data['url_login'] = reverse('login')
        return data


class AutorizacionTemplateView(AuthMercadoLibreMixin, generic.TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        _redir = 'http://localhost:8000' + reverse('autorizacion')
        access, refresh = self.mercadolibre.authorize(self.request.GET.get('code'), _redir)
        self.request.session[settings.MERCADO_LIBRE_APP_ACCESS_TOKEN] = access
        self.request.session[settings.MERCADO_LIBRE_APP_REFRESH_TOKEN] = refresh
        params = {'access_token': self.mercadolibre.access_token}
        self.request.session[settings.MERCADO_LIBRE_APP_USER_INFO] = query.User.myinfo(_handler=self.mercadolibre,
                                                                                       params=params)
        return redirect(reverse('home'))

    def get_context_data(self, **kwargs):
        data = super(AutorizacionTemplateView, self).get_context_data(**kwargs)
        data['url_login'] = self.url_login
        return data



class HomeTemplateView(AuthMercadoLibreMixin, generic.TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        data = super(HomeTemplateView, self).get_context_data(**kwargs)
        return data