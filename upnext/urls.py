from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^see_all/$', views.see_all_parties, name='see_all'),
    url(r'^(?P<party_name>[a-z0-9-_]+)/$', views.party, name='party'),
]
