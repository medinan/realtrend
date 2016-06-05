# --encoding:utf-8

from mercadolibre.lib.meli import Meli
from django.conf import settings
from functools import wraps
from django.core.urlresolvers import reverse

handler_app = Meli(client_id=settings.MERCADO_LIBRE_APP_ID,
                   client_secret=settings.MERCADO_LIBRE_APP_SECRET_KEY)


# class AuthDataSetting():




class AjaxMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.is_ajax():
            return self.ajax(request, *args, **kwargs)
        return super(AjaxMixin, self).dispatch(request, *args, **kwargs)


class AuthMercadoLibreMixin(object):
    @classmethod
    def as_view(cls, **kwargs):
        return super(AuthMercadoLibreMixin, cls).as_view(**kwargs)

    def is_auth(self):
        if self.request.session.get('auth_token'):
            return True
        else:
            return False

    @property
    def url_login(self):
        _re = 'http://localhost:8000' + reverse('autorizacion')
        url = handler_app.auth_url(redirect_URI=_re)
        return url

    @property
    def url_redirect(self):
        return 'http://localhost:8000' + reverse('ingreso')

    def get_context_data(self, **kwargs):
        data = super(AuthMercadoLibreMixin, self).get_context_data(**kwargs)
        return data


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

