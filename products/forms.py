# --encoding: utf-8

from django import forms
from api.utils import ML_EXTRA_FIELD
import json


class PublicationsCreate(forms.Form):
    title = forms.CharField(max_length=400, label='Titulo',
                            widget=forms.TextInput(attrs={'placeholder': 'Titulo'}))

    condition = forms.ChoiceField(choices=[], label='Condicion',
                                  widget=forms.Select(attrs={'palceholder': 'Condicion'}))
    currency_id = forms.ChoiceField(choices=[], required=True, label='Currency',
                            widget=forms.Select(attrs={'placeholder': 'Currency'}))
    listing_type_id = forms.ChoiceField(choices=[], required=True, label='Tipo publicacion',
                            widget=forms.Select(attrs={'placeholder': 'Tipo publicacion'}))
    available_quantity = forms.IntegerField(min_value=1, label='Cantidad',
                            widget=forms.TextInput(attrs={'placeholder': 'Cantidad'}))
    price = forms.DecimalField(min_value=1.0, decimal_places=2, label='Precio',
                            widget=forms.TextInput(attrs={'placeholder': 'Precio'}))

    def __init__(self, *args, **kwargs):
        currencies = kwargs.pop('currencies')
        attributes = kwargs.pop('attributes')
        listing_type = kwargs.pop('listing_type')
        category = kwargs.pop('category')

        super(PublicationsCreate, self).__init__( *args, **kwargs)
        self.fields['currency_id'].choices = [(c['id'], c['description']) for c in currencies \
                                              if c['id'] in category['settings']['currencies']]
        self.fields['listing_type_id'].choices = [(c['id'], c['name']) for c in listing_type]
        self.fields['listing_type_id'].initial = 'free'
        self.fields['condition'].choices = [(s, s) for s in category['settings']['item_conditions']]
        self.dinamic_field = []
        if attributes:
            for item in attributes:
                if item['tags'].get('required', False):
                    self.dinamic_field.append(item)
                    self.fields[item['name']] = ML_EXTRA_FIELD[item['value_type']](**item)

    def save(self):
        data = self.clean()
        return data

    def clean(self):
        _data = self.data.dict()
        del _data['csrfmiddlewaretoken']
        attributes = []
        for f in self.dinamic_field:
            attributes.append({'id': f['id'], 'value': _data[f['name']]})
            del _data[f['name']]
        if attributes:
            _data['attributes'] = attributes
        return _data


