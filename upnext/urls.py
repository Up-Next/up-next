from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^find_or_create/$', views.find_or_create_party, name='search'),
    url(r'^(?P<party_name>[a-z0-9-_]+)/$', views.party, name='party'),
]
