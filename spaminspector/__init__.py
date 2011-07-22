# vim: fileencoding=utf8 :
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

if not hasattr(settings, 'SPAMINSPECTOR_AKISMET_KEY'):
    raise ImproperlyConfigured("You must define the SPAMINSPECTOR_AKISMET_KEY setting.")

# Default SPAMINSPECTOR_VIEWS is for django comment framework
settings.SPAMINSPECTOR_VIEWS = getattr(settings, 'SPAMINSPECTOR_VIEWS', (
    ('django.contrib.comments.views.comments.post_comment', {
        'comment_type': 'comment',
        'comment_author': lambda request: request.POST.get('name', ""),
        'comment_author_email': lambda request: request.POST.get('email', ""),
        'comment_author_url': lambda request: request.POST.get('url', ""),
        'comment_contents': lambda request: request.POST.get('comment', ""),
    }),
))
settings.SPAMINSPECTOR_SPAM_TEMPLATE = getattr(settings, 'SPAMINSPECTOR_SPAM_TEMPLATE', '')