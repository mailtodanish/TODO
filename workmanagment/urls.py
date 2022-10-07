from django.contrib import admin
from django.conf.urls import *


urlpatterns =  [
    url(r'^admin/', admin.site.urls),
    url(r'', include('projects.urls')),
    url(r'', include('api.urls')),
    url('^', include('django.contrib.auth.urls')),
    
]
