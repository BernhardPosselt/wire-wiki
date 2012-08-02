#!/usr/bin/env python
#-*- coding:utf-8 -*-

import json
import markdown

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from wire.wiki.models import WikiPage, WikiPageModification
from wire.wiki.forms import WikiPageForm, WikiPageModificationForm


@login_required
def index(request):
    pages = WikiPage.objects.all()
    ctx = {
        'pages': pages,
    }
    return render(request, 'wiki/index.html', ctx)


@login_required
def page(request, id):
    page = get_object_or_404(WikiPage, pk=id)
    modifications = WikiPageModification.objects.filter(page__id=id)
    if len(modifications) > 0:
        latest_modification = modifications[0]
        html = markdown.markdown(latest_modification.content.encode("UTF-8"))
    else:
        html = ''

    ctx = {
        'page': page,
        'html': html
    }
    return render(request, 'wiki/page.html', ctx)


@login_required
def page_new(request):
    if request.method == 'POST':
        form = WikiPageForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('wiki:index'))
    else:
        form = WikiPageForm()
    ctx = {
        'form': form,
    }
    return render(request, 'wiki/page_new.html', ctx)


@login_required
def page_edit(request, id):
    page = get_object_or_404(WikiPage, pk=id)
    modifications = WikiPageModification.objects.filter(page__id=id)

    if request.method == 'POST':
        form = WikiPageModificationForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.page = page
            form.save()
            return HttpResponseRedirect(reverse('wiki:index'))

    else:
        if len(modifications) > 0:
            form = WikiPageModificationForm(instance=modifications[0])
        else:
            form = WikiPageModificationForm()

    ctx = {
        'form': form,
        'page': page,
        'modifications': modifications,
    }
    return render(request, 'wiki/page_edit.html', ctx)


@login_required
def page_delete(request, id):
    page = get_object_or_404(WikiPage, pk=id)

    if request.method == 'POST':
        page.delete()
        return HttpResponseRedirect(reverse('wiki:index'))

    ctx = {
        'page': page,
    }
    return render(request, 'wiki/page_delete.html', ctx)


@login_required
def js_settings(request):
    settings = {
        #'wiki_index_url': reverse('wiki:index'),
    }
    return HttpResponse(json.dumps(settings), mimetype='application/json')


@login_required
def logout_to_index(request):
    logout(request)
    return HttpResponseRedirect(reverse('wiki:index'))
