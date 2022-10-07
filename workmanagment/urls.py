from django.contrib import admin
from django.urls import *


urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'', include('projects.urls')),
    re_path(r'', include('api.urls')),
    re_path('^', include('django.contrib.auth.urls')),

]
