# --encoding: utf-8

from django.views import generic
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
# Create your views here.


class PublicacionSelectCategoryView(CategoryMixin, generic.FormView):
    template_name = 'publications_create.html'
    form_class = frm_products.PublicationsCreate

    def get_context_data(self, **kwargs):
        data = super(PublicacionSelectCategoryView, self).get_context_data(**kwargs)
        data['categorys'] = self.get_list_category()
        data['root_category'] = self.is_category_root
        data['is_leaf'] = False if self.is_category_root or \
                                   data['categorys'].get('children_categories')!=[] else True
        return data


class ProductosPublicadosView(AuthMercadoLibreMixin, generic.ListView):
    pass


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
