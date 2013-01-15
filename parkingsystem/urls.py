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
    url(r'^admin/', include(admin.site.urls)),
    (r'^register/$', 'parker.views.ParkerRegistration'),
    (r'^login/$', 'parker.views.LoginRequest'),
    (r'^logout/$', 'parker.views.LogoutRequest'),
    url(r'^profile/', 'parker.views.Profile'),
    url(r'^parking/','home.views.parking_status'),
    url(r'^gcheckout/','home.views.guest_check_out'),
    url(r'^ucheckout/','home.views.user_check_out'),
    url(r'^ucheckin/','home.views.user_check_in'),
    url(r'^gcheckin/','home.views.guest_check_in'),
    url(r'^pricing/', 'home.views.pricing'),
)
