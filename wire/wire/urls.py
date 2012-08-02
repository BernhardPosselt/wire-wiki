#!/usr/bin/env python
#-*- coding:utf-8 -*-

# Django imports
from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# uncomment for enabling admin
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()

# generate top url for appending to urls
project_url = ''
if len(settings.PROJECT_URL) > 1:
    project_url = settings.PROJECT_URL[1:] + '/'

urlpatterns += patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    url(r'^' + project_url, include('wire.wiki.urls', namespace='wiki', app_name='wiki')),
)
