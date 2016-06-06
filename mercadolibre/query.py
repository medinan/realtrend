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
    def myitems(_handler, user_id, params):
        path = 'users/%s/items/search' % user_id
        _result = _handler.get(path, params)
        return json.loads(_result.content)
    @staticmethod
    def mylistitem(_handler, params):
        path = '/items'
        _result = _handler.get(path, params)
        return json.loads(_result.content)
    @staticmethod
    def additem(_handler, body, params):
        path = '/items'
        _result = _handler.post(path=path, body=body, params=params)
        return _result.status_code, json.loads(_result.content)


class Sites(object):
    @staticmethod
    def get_root_category(_handler, params):
        path = '/sites/%s/categories' % settings.MERCADO_LIBRE_APP_SITES['id']
        _result = _handler.get(path, params)
        return json.loads(_result.content)

    @staticmethod
    def get_sub_category(_handler, categoria):
        path = '/categories/%s' % categoria
        _result = _handler.get(path)
        return json.loads(_result.content)

    @staticmethod
    def get_category_attributes(_handler, categoria):
        path = 'categories/%s/attributes' % categoria
        _result = _handler.get(path)
        return json.loads(_result.content)

    @staticmethod
    def get_currency(_handler,params={}):
        path = 'currencies/'
        _result = _handler.get(path, params)
        return json.loads(_result.content)

    @staticmethod
    def get_listing_type(_handler, params):
        path = 'sites/%s/listing_types' % settings.MERCADO_LIBRE_APP_SITES['id']
        _result = _handler.get(path, params)
        return json.loads(_result.content)






