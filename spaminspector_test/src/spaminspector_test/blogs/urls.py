# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

from django.views.generic import ListView
from django.views.generic import DetailView

from models import Entry

kwargs = {
    'queryset': Entry.objects.all(),
}

urlpatterns = patterns('',
    url(r'^$', ListView.as_view(**kwargs), name='blogs-entry-list'),
    url(r'^(?P<pk>\d+)/$', DetailView.as_view(**kwargs), name='blogs-entry-detail'),
)