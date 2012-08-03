#!/usr/bin/env python
#-*- coding:utf-8 -*-

from wire.wiki.models import WikiPage, WikiPageModification
from django.contrib import admin


class WikiPageAdmin(admin.ModelAdmin):
    list_display = ['title', 'created']
    ordering = ['-created']
    search_fields = ['title']
    list_filter = ['created']
    date_hierarchy = 'created'


class WikiPageModificationAdmin(admin.ModelAdmin):
    list_display = ['description', 'page', 'user', 'timestamp']
    ordering = ['-timestamp']
    search_fields = ['description', 'page', 'user']
    list_filter = ['timestamp', 'user', 'page']
    date_hierarchy = 'timestamp'


admin.site.register(WikiPage, WikiPageAdmin)
admin.site.register(WikiPageModification, WikiPageModificationAdmin)
