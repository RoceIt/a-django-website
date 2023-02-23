from django.conf.urls import url

from . import views

app_name = 'food'

urlpatterns = [
    url(r'^all$', views.FoodProductList.as_view(), name='all'),
    url(r'(?P<pk>[0-9]+)/$', views.FoodProductDetail.as_view(), name='detail'),
]
