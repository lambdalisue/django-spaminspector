# -*- coding: utf-8 -*-
#
# from snippets: http://djangosnippets.org/snippets/1054/
#
from django.contrib import admin
from models import Entry

class EntryAdmin(admin.ModelAdmin):
    date_hierarchy  = 'created_at'
    list_display = ('title', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('title', 'body',)
    
admin.site.register(Entry, EntryAdmin)
