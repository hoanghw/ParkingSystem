from django.conf.urls import patterns, include, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'parkingsystem.views.home', name='home'),
    # url(r'^parkingsystem/', include('parkingsystem.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^parking/','home.views.parking_status'),
    url(r'^gcheckout/','home.views.guest_check_out'),
    url(r'^ucheckout/','home.views.user_check_out'),
    url(r'^response/','home.views.response'),
    url(r'^ucheckin/','home.views.user_check_in'),
    url(r'^gcheckin/','home.views.guest_check_in'),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
