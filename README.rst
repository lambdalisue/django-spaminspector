Django's genetic spam inspector library via Akismet


Install
===========================================

	sudo pip install django-spaminspector

or

    sudo pip install git+git://github.com/lambdalisue/django-spaminspector.git#egg=django-spaminspector


How to Use
==========================================

1.	First, you need to specified ``SPAMINSPECTOR_AKISMET_KEY`` on ``settings.py``
2.  Add ``spaminspector`` to ``INSTALLED_APPS`` on ``settings.py``
3.  Add ``spaminspector.middleware.SpamInspectionMiddleware`` to ``MIDDLEWARE_CLASSES`` on ``settings.py``
4.  Add view which you want to inspect to ``SPAMINSPECTOR_VIEWS``
    The code below is a profile for django's comment framework::

        SPAMINSPECTOR_VIEWS = (
            ('django.contrib.comments.views.comments.post_comment', {
                'comment_type': 'comment',
                'comment_author': lambda request: request.POST.get('name', ""),
                'comment_author_email': lambda request: request.POST.get('email', ""),
                'comment_author_url': lambda request: request.POST.get('url', ""),
                'comment_contents': lambda request: request.POST.get('comment', ""),
            }),
        )

Settings
=========================================
``SPAMINSPECTOR_VIEWS``
    the list of view and inspection_profile. default settings is for django comment framework.

``SPAMINSPECTOR_AKISMET_KEY``
    the api key of Akismet of your url.

``SPAMINSPECTOR_SPAM_TEMPLATE``
    an template uri. this template is used to show when comment is detected as spam. (optional)
