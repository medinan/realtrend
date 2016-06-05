import json
from django.conf import settings

class User(object):

    @staticmethod
    def myinfo(_handler, params):
        path = '/users/me'
        _result = _handler.get(path, params)
        return json.loads(_result.content)


class UserItems(object):

    @staticmethod
    def myitems(_handler, params):
        path = '/items'
        _result = _handler.get(path, params)
        return json.loads(_result.content)


class Sites(object):
    @staticmethod
    def get_root_category(_handler, params):
        path = '/sites/%s/categories' % settings.MERCADO_LIBRE_APP_SITES['id']
        _result = _handler.get(path, params)
        return json.loads(_result.content)



