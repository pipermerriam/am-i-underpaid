# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView


urlpatterns = patterns(
    '',
    url(
        r'^$', TemplateView.as_view(template_name='home.html'),
        name="home",
    ),
    # Salaries
    url(r'^salary/', include('disparity.apps.salary.urls')),
)


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
