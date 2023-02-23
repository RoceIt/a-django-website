from django.conf import settings
from django.db import models

# Create your models here.
def named_patterns_list():
    pass





def root_url_pattern():
    root_url_pattern = root_url_conf.urls.urlpatterns
    return root_url_pattern


root_url_conf = __import__(settings.ROOT_URLCONF)
