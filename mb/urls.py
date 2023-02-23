"""mb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.index, name='mb_home'),
    url(r'^products/', include('food.urls')),
    url(r'^client/', include('client.urls')),
    url(r'^orders/', include('orders.urls')),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^address/', include('address.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^staff_menu$', views.staff_management, name='staff_menu'),
    url(r'^_ah/healt',views.default_google_heath_check),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler403 = views.index


# Changing the admin site branding
admin.site.site_header = 'Madame Bocale beheer'
admin.site.site_title = 'MB beheer'
admin.site.site_index = 'Algemeen site beheer'
