# --encoding: utf-8

from django.views import generic
from django.conf import settings
from django.db import transaction
from products import models as pro_models
from products import forms as prod_forms
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from api.utils import AjaxMixin
from django.db.models import Q
from django.template.loader import render_to_string
from django.http import JsonResponse
from api.utils import AuthMercadoLibreMixin, CategoryMixin
from mercadolibre import query
from products import forms as frm_products
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
# Create your views here.


class PublicationSelectCategoryView(CategoryMixin, generic.TemplateView):
    template_name = 'publications_select_category.html'

    def get_context_data(self, **kwargs):
        data = super(PublicationSelectCategoryView, self).get_context_data(**kwargs)
        data['categorys'] = self.get_list_category()
        data['current_category'] = self.get_current_category()
        data['root_category'] = self.is_category_root
        data['is_leaf'] = False if self.is_category_root or \
                                   data['categorys'].get('children_categories')!=[] else True
        return data


class PublicationCreateView(CategoryMixin, generic.FormView):
    template_name = 'publications_create.html'
    form_class = frm_products.PublicationsCreate

    def get_current_category(self):
        return self.kwargs['category']

    def get_form(self, form_class=None):
        currencies = query.Sites.get_currency(self.mercadolibre, params={})
        attributes = query.Sites.get_category_attributes(self.mercadolibre, self.get_current_category())
        listing_type = query.Sites.get_listing_type(self.mercadolibre, params={})
        category = query.Sites.get_sub_category(self.mercadolibre, self.get_current_category())
        if self.request.method == 'GET':
            return self.form_class(currencies=currencies, attributes=attributes,
                                   listing_type=listing_type, category=category)
        else:
            return self.form_class(self.request.POST, currencies=currencies, attributes=attributes,
                                   listing_type=listing_type, category=category)

    def form_valid(self, form):
        body = form.save()
        body.update(category_id=self.get_current_category())
        status, _result = query.UserItems.additem(self.mercadolibre, body,
                                          params={'access_token': self.mercadolibre.access_token})
        if status == 201:
            messages.success(self.request, 'La publicacion se genero exitosa!!!')
            return redirect(reverse('publications_list'))
        else:
            messages.error(self.request, "%s %s" % (_result['message'], _result['error']))
            for causes in _result['cause']:
                messages.error(self.request, "%s, %s" % (causes['code'], causes['message']))
            return super(PublicationCreateView, self).form_invalid(form=form)

    def get_context_data(self, **kwargs):
        data = super(PublicationCreateView, self).get_context_data(**kwargs)
        data['category'] = query.Sites.get_sub_category(self.mercadolibre, self.get_current_category())
        return data


class ProductosPublicadosView(CategoryMixin, generic.ListView):
    template_name = 'publications_list.html'

    def get_queryset(self):
        _result = query.UserItems.myitems(self.mercadolibre,
                                          self.request.session[settings.MERCADO_LIBRE_APP_USER_INFO]['id'],
                                          params={'access_token': self.mercadolibre.access_token})
        _product = query.UserItems.mylistitem(self.mercadolibre, params={'ids': ','.join(_result['results'])})
        for idx in range(len(_product)):
            _product[idx]['category'] = query.Sites.get_sub_category(self.mercadolibre,
                                                                     _product[idx]['category_id'])

        return _product

    def get_context_data(self, **kwargs):
        data = super(ProductosPublicadosView, self).get_context_data(**kwargs)
        return data



# class IngresoTemplateView(generic.TemplateView):
#     template_name = 'index.html'
#
#     def get_context_data(self, **kwargs):
#         data = super(IngresoTemplateView, self).get_context_data(**kwargs)


# class CatalogFormView(AjaxMixin, generic.FormView):
#     template_name = 'catalog.html'
#     form_class = prod_forms.ProductForm
#
#     def form_valid(self, form):
#         form.save()
#         super(CatalogFormView, self).form_valid(form)
#         return redirect(self.get_success_url())
#
#     def get_success_url(self):
#         return reverse('catalog_products')
#
#     def get_form(self, form_class=None):
#         if self.request.method == 'POST':
#             return self.form_class(self.request.POST)
#         return self.form_class()
#
#     def ajax(self, request, *args, **kwargs):
#         action = request.GET.get('action')
#         response = {}
#         if action == 'filter':
#             filter_by = request.GET.get('filter')
#             query = pro_models.Product.objects.filter(Q(code__icontains=filter_by) | Q(name__icontains=filter_by))
#             response = {'html': render_to_string(template_name='filter_products.html', context={'products': query})}
#         elif action == 'save':
#             pk, code, name, quantity = request.GET.get('pk'), request.GET.get('code'), \
#                                        request.GET.get('name'), request.GET.get('quantity')
#
#             valid = pk and name and code and quantity
#             if valid:
#                 pro_models.Product.objects.filter(pk=pk).update(code=code, name=name, quantity=quantity)
#                 response = {'update': 200}
#             else:
#                 response = {'update': 500}
#
#         return JsonResponse(response)
#
#     def get_context_data(self, **kwargs):
#         data = super(CatalogFormView, self).get_context_data(**kwargs)
#         data['products'] = pro_models.Product.objects.all()
#         return data
