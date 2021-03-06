#!/usr/bin/env python
#-*- coding:utf-8 -*-

import json
import difflib
import markdown

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _

from wire.wiki.models import WikiPage, WikiPageModification
from wire.wiki.forms import WikiPageForm, WikiPageModificationForm


@login_required
def index(request):
    pages = WikiPage.objects.all()
    if len(pages) > 0:
        try:
            page = WikiPage.objects.get(title="Index")
            return HttpResponseRedirect(reverse('wiki:page', args=[page.id]))
        except WikiPage.DoesNotExist:
            return HttpResponseRedirect(reverse('wiki:pages'))
    else:
        return HttpResponseRedirect(reverse('wiki:pages'))


@login_required
def pages(request):
    pages = WikiPage.objects.all()
    index_page = WikiPage.objects.filter(title="Index")
    if len(index_page) > 0:
        index_page_exists = True
    else:
        index_page_exists = False

    ctx = {
        'pages': pages,
        'index_page_exists': index_page_exists
    }
    return render(request, 'wiki/pages.html', ctx)


@login_required
def page_changelog(request, page_id):
    changes = WikiPageModification.objects.filter(page=page_id)
    ctx = {
        'changes': changes,
    }
    return render(request, 'wiki/changelog.html', ctx)


@login_required
def changelog(request):
    changes = WikiPageModification.objects.all()
    ctx = {
        'changes': changes,
    }
    return render(request, 'wiki/changelog.html', ctx)


@login_required
def changelog_detail(request, change_id):
    current_change = get_object_or_404(WikiPageModification, pk=change_id)
    page = current_change.page

    current_change_lines = current_change.content.splitlines()
    previous_change_lines = []

    try:
        previous_change = WikiPageModification.objects.filter(pk__lt=change_id, page=page.id).latest('timestamp')
        previous_change_lines = previous_change.content.splitlines()
    except WikiPageModification.DoesNotExist:
        previous_change = False

    # build diff
    diff = []
    for diff_line in difflib.context_diff(previous_change_lines, current_change_lines):
        if diff_line.strip().startswith("+"):
            css_class = "added"
        elif diff_line.strip().startswith("---"):
            css_class = "seperator"
        elif diff_line.strip().startswith("-"):
            css_class = "deleted"
        elif diff_line.strip().startswith("!"):
            css_class = "modified"
        else:
            css_class = ""
        line = {
            'diff': diff_line,
            'css_class': css_class,
        }
        diff.append(line)

    source = current_change.content
    html = markdown.markdown(unicode(source))
    ctx = {
        'page': page,
        'change': current_change,
        'previous_change': previous_change,
        'html': html,
        'diff': diff,
        'source': source
    }
    return render(request, 'wiki/changelog_detail.html', ctx)


@login_required
def page(request, page_id):
    page = get_object_or_404(WikiPage, pk=page_id)
    modifications = WikiPageModification.objects.filter(page__id=page_id)
    if len(modifications) > 0:
        latest_modification = modifications[0]
        last_update = latest_modification.timestamp
        html = markdown.markdown(unicode(latest_modification.content))
    else:
        last_update = False
        html = u''

    ctx = {
        'page': page,
        'html': html,
        'last_update': last_update
    }
    return render(request, 'wiki/page.html', ctx)


@login_required
def page_new(request):
    title = request.GET.get('title', '')
    if request.method == 'POST':
        form = WikiPageForm(request.POST)
        if form.is_valid():
            form = form.save()
            return HttpResponseRedirect(reverse('wiki:page_edit', args=[form.id]))
    else:
        initial = {
            'title': title
        }
        form = WikiPageForm(initial=initial)
    ctx = {
        'form': form
    }
    return render(request, 'wiki/page_new.html', ctx)


@login_required
def page_edit(request, page_id):
    page = get_object_or_404(WikiPage, pk=page_id)
    modifications = WikiPageModification.objects.filter(page__id=page_id)

    edit_warning = ''
    # get the current latest modifcation
    try:
        previous_change_id = WikiPageModification.objects.filter(page=page_id).latest('timestamp').id
    except WikiPageModification.DoesNotExist:
        previous_change_id = 0

    if request.method == 'POST':
        # check if the id via post is the currently latest change
        if previous_change_id != int(request.POST.get('previous_change_id')):
            edit_warning = _("Your page was edited by someone else before you could save. \
                Please copy all your changes, reload this page and merge them with the current version.")
        print "DB %s POST %s" % (previous_change_id, request.POST.get('previous_change_id'))
        form = WikiPageModificationForm(request.POST)
        if form.is_valid() and edit_warning == '':
            form = form.save(commit=False)
            form.user = request.user
            form.page = page
            form.save()
            return HttpResponseRedirect(reverse('wiki:page', args=[page_id]))

    else:
        if len(modifications) > 0:
            form = WikiPageModificationForm(instance=modifications[0])
        else:
            form = WikiPageModificationForm()

    ctx = {
        'form': form,
        'page': page,
        'modifications': modifications,
        'previous_change_id': previous_change_id,
        'edit_warning': edit_warning
    }
    return render(request, 'wiki/page_edit.html', ctx)


@login_required
def page_delete(request, page_id):
    page = get_object_or_404(WikiPage, pk=page_id)

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
