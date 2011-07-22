#!/usr/bin/env python
# vim: set fileencoding=utf8 :
"""Django Inspector middleware

Methods:
    foobar - the explanation of the method.

Data:
    hogehoge - the explanation of the data.


Copyright:
    Copyright 2011 Alisue allright reserved.

License:
    Licensed under the Apache License, Version 2.0 (the "License"); 
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unliss required by applicable law or agreed to in writing, software
    distributed under the License is distrubuted on an "AS IS" BASICS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
__author__  = 'Alisue <lambdalisue@hashnote.net>'
__version__ = '1.0.0'
__date__    = '2011-07-22'
from django.conf import settings
from django.http import HttpResponseForbidden
from django.template.response import TemplateResponse
from django.contrib.sites.models import Site
from django.core.urlresolvers import get_callable
from django.core.exceptions import MiddlewareNotUsed
from akismet import Akismet

import warnings

class SpamInspectionMiddleware(object):
    
    def __init__(self):
        # Create Akismet instance and check whether the API key is valid or not
        kwargs = {
            'key': settings.SPAMINSPECTOR_AKISMET_KEY,
            'blog_url': "http://%s/" % Site.objects.get(pk=settings.SITE_ID).domain,
        }
        self.akismet = Akismet(**kwargs)
        if not self.akismet.verify_key():
            warnings.warn("Your SPAMINSPECTOR_AKISMET_KEY is invalid. Spam inspection feture is turned off.")
            raise MiddlewareNotUsed
        # Create inspection_views dict
        self.inspection_views = {}
        for view_func, profile in settings.SPAMINSPECTOR_VIEWS:
            if isinstance(view_func, basestring):
                # Load view_func from string
                view_func = get_callable(view_func)
            self.inspection_views[view_func] = profile
    
    def _is_spam(self, request, profile):
        def _get(request, profile, key):
            value = profile.get(key, "")
            if callable(value):
                value = value(request)
            if isinstance(value, unicode):
                value = value.encode('utf-8')
            return value
        data = {
            'user_ip': request.META.get('REMOTE_ADDR', '127.0.0.1'),
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
            'referrer': request.META.get('HTTP_REFERER', ''),
            'comment_type': _get(request, profile, 'comment_type'),
            'comment_author': _get(request, profile, 'comment_author'),
            'comment_email': _get(request, profile, 'comment_email'),
            'comment_url': _get(request, profile, 'comment_url'),
        }
        contents = _get(request, profile, 'comment_contents')
        return self.akismet.comment_check(contents, data, build_data=True)
        
    def process_view(self, request, view_func, view_args, view_kwargs):
        if view_func in self.inspection_views.keys():
            # Check spamness of request
            inspection_profile = self.inspection_views[view_func]
            if self._is_spam(request, inspection_profile):
                # Detected as spam
                if settings.SPAMINSPECTOR_SPAM_TEMPLATE:
                    return TemplateResponse(request, settings.SPAMINSPECTOR_SPAM_TEMPLATE, status=403)
                else:
                    return HttpResponseForbidden("You comment was detected as SPAM")
        return view_func(request, *view_args, **view_kwargs)
