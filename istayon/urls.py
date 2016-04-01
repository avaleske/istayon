from django.conf.urls import patterns, include, url
from django.contrib import admin

import istayon.views


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'istayon.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^tos', istayon.views.tos, name="tos"),
    url(r'^supporters', istayon.views.supporters, name="supporters"),
    url(r'^honestly', istayon.views.index, name="index"),
    url(r'^$', istayon.views.aprilfools, name="aprilfools"),
)

handler404 = 'istayon.views.page_not_found'
