# --encoding:utf-8

from mercadolibre.lib.meli import Meli
from mercadolibre import query
from django.conf import settings
from functools import wraps
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site


class AjaxMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.is_ajax():
            return self.ajax(request, *args, **kwargs)
        return super(AjaxMixin, self).dispatch(request, *args, **kwargs)


class AuthMercadoLibreMixin(object):
    """
    Clase Mixin multiproposito para administracion de autentizacion y autorizacion.

    """
    @classmethod
    def as_view(cls, **kwargs):
        return super(AuthMercadoLibreMixin, cls).as_view(**kwargs)

    def is_auth(self):
        if self.request.session.get(settings.MERCADO_LIBRE_APP_ACCESS_TOKEN):
            return True
        else:
            return False

    def get_access_token(self):
        return self.request.session[settings.MERCADO_LIBRE_APP_ACCESS_TOKEN]

    def get_refresh_token(self):
        return self.request.session[settings.MERCADO_LIBRE_APP_REFRESH_TOKEN]

    @property
    def mercadolibre(self):
        if self.is_auth():
            return Meli(client_id=settings.MERCADO_LIBRE_APP_ID, client_secret=settings.MERCADO_LIBRE_APP_SECRET_KEY,
                        access_token=self.get_access_token(), refresh_token=self.get_refresh_token())
        else:
            return Meli(client_id=settings.MERCADO_LIBRE_APP_ID, client_secret=settings.MERCADO_LIBRE_APP_SECRET_KEY)

    @property
    def user_info(self):
        return self.request.session.get(settings.MERCADO_LIBRE_APP_USER_INFO)

    @property
    def url_login(self):
        site = Site.objects.get_current()
        _re = 'http://' + site.domain + reverse('autorizacion')
        url = self.mercadolibre.auth_url(redirect_URI=_re)
        return url

    @property
    def url_redirect(self):
        site = Site.objects.get_current()
        return site.domain + reverse('ingreso')

    def get_context_data(self, **kwargs):
        data = super(AuthMercadoLibreMixin, self).get_context_data(**kwargs)
        data['user'] = self.user_info
        data['is_auth'] = self.is_auth()
        return data


class CategoryMixin(AuthMercadoLibreMixin):
    def get_current_category(self):
        return self.request.GET.get('category')

    @property
    def is_category_root(self):
        if self.get_current_category():
            return False
        else:
            return True

    def get_list_category(self):
        if not self.request.GET.get('category'):
            _cat = query.Sites.get_root_category(_handler=self.mercadolibre, params={})
        else:
            _cat = query.Sites.get_sub_category(_handler=self.mercadolibre, categoria=self.request.GET['category'])
        return _cat


def login_required(url_login):
    """Metodo decorador check_roles verifica que el usuario tenga los roles necesarios
    para acceder a la vista. En caso de que no posea los permisos retorna PermissionDenied object.

    """
    def _login_required(view_func):
        @wraps(view_func)
        def __login_required(view, *args, **kwargs):

            for rol in view.roles_required:
                if rol in my_roles:
                    pass
                else:
                    raise PermissionDenied

            return view_func(view, *args, **kwargs)

        return __login_required
    return _login_required

