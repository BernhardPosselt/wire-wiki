#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _


class WikiPage(models.Model):
    title = models.CharField(_(u"Title"), max_length=100)
    created = models.DateTimeField(_(u"Created"), auto_now_add=True)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _(u"WikiPage")
        verbose_name_plural = _(u"WikiPages")
        ordering = ['-created']


class WikiPageModification(models.Model):
    page = models.ForeignKey("WikiPage")
    content = models.TextField(_(u"Content"), blank=True)
    description = models.CharField(_(u"Description"), default=_("Minor Change"),
        blank=True, max_length=100)
    timestamp = models.DateTimeField(_(u"Created"), auto_now_add=True)
    user = models.ForeignKey("auth.User")

    def __unicode__(self):
        return self.description

    class Meta:
        verbose_name = _(u"WikiPage Modification")
        verbose_name_plural = _(u"WikiPage Modifications")
        ordering = ['-timestamp']


#class UserProfile(models.Model):
#    user = models.OneToOneField("auth.User")
