from django.conf.urls import url

from . import views

app_name = 'choicemenu'

urlpatterns = [
    url(r'^full_url_conf$', views.full_url_conf, name='named_patterns'),
]
