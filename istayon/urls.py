from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
import istayon.views
import apipoll.views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'istayon.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', apipoll.views.index, name="index"),
    # url(
    #     r'^favicon.ico$',
    #     RedirectView.as_view(
    #         url=staticfiles_storage.url('favicon.ico'),
    #         permanent=False),
    #     name="favicon"
    # ),

)
