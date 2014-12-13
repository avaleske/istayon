from django.conf.urls import patterns, include, url
from django.contrib import admin
import istayon.views
import apipoll.views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'istayon.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', apipoll.views.index, name="index"),
    url(r'^reload/$', apipoll.views.reload_data, name="reload"),
)
