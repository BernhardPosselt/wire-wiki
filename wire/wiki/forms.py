#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django import forms
#from django.utils.translation import ugettext_lazy as _

from wire.wiki.models import WikiPage, WikiPageModification


class WikiPageForm(forms.ModelForm):
    class Meta:
        model = WikiPage


class WikiPageModificationForm(forms.ModelForm):
    class Meta:
        model = WikiPageModification
        exclude = ('user', 'page')
