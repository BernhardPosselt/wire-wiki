#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.conf.urls.defaults import *
#from django.views.generic import TemplateView

urlpatterns = patterns('wire.wiki.views.main',
    url(r'^$', 'index', name='index'),
    url(r'^pages/$', 'pages', name='pages'),
    url(r'^page/(?P<page_id>\d+)/$', 'page', name='page'),
    url(r'^page/new/$', 'page_new', name='page_new'),
    url(r'^page/edit/(?P<page_id>\d+)/$', 'page_edit', name='page_edit'),
    url(r'^page/delete/(?P<page_id>\d+)/$', 'page_delete', name='page_delete'),
    url(r'^page/(?P<page_id>\d+)/changelog/$', 'page_changelog', name='page_changelog'),

    url(r'^changelog/$', 'changelog', name='changelog'),
    url(r'^changelog/(?P<change_id>\d+)/$', 'changelog_detail', name='changelog_detail'),

    url(r'^js/settings/', 'js_settings', name='js_settings'),
    url(r'^logout/', 'logout_to_index', name='logout_to_index'),
    #url(r'^sitenotice/', #TemplateView.as_view(template_name="wiki/sitenotice.html")),
)

urlpatterns += patterns('django.contrib.auth.views',
    url(r'^login/$', 'login', {'template_name': 'wiki/login.html'},
        name='login'),
)

