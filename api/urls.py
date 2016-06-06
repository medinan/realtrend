"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from api import views as api_views
from products import views as prod_views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', api_views.IndexTemplateView.as_view(), name='ingreso'),
    url(r'^autorizacion/$', api_views.AutorizacionTemplateView.as_view(), name='autorizacion'),
    url(r'^login/$', api_views.LoginRedirectView.as_view(), name='login'),
    url(r'^home/$', api_views.HomeTemplateView.as_view(), name='home'),
    url(r'^products/(?P<category>[\w_-]+)/new/$', prod_views.PublicationCreateView.as_view(), name='publications_create'),
    url(r'^products/create/$', prod_views.PublicationSelectCategoryView.as_view(), name='publications_category_select'),
    url(r'^products/list/$', prod_views.ProductosPublicadosView.as_view(), name='publications_list'),


]
