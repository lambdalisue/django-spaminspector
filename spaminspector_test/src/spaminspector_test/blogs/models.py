# -*- coding: utf-8 -*-
from django.db import models

class Entry(models.Model):
    """Simple Blog Entry model"""
    title = models.CharField("title", max_length=128)
    body = models.TextField("body")
    created_at = models.DateTimeField("date created", auto_now_add=True)
    updated_at = models.DateTimeField("date updated", auto_now=True)
    
    class Meta:
        ordering = ('-created_at',)
        verbose_name = "entry"
        verbose_name_plural = "entries"
    
    def __unicode__(self):
        return self.title
    
    @models.permalink
    def get_absolute_url(self):
        return ("blogs-entry-detail", (self.pk,))