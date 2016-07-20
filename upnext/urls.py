from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create/$', views.create, name='create'),
    url(r'^see_all/$', views.see_all_parties, name='see_all'),
    url(r'^successfully_created/$', views.successfully_created, name='successful'),
]
