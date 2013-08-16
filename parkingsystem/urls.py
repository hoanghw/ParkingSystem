from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'parkingsystem.views.home', name='home'),
    # url(r'^parkingsystem/', include('parkingsystem.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^$','dummyAPIs.views.ulogin'),
    url(r'^checkticket/$','home.views.check_ticket'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^register/$', 'parker.views.ParkerRegistration'),
    url(r'^login/$', 'parker.views.LoginRequest'),
    url(r'^logout/$', 'parker.views.LogoutRequest'),
    url(r'^profile/', 'parker.views.Profile'),
    url(r'^parking/','home.views.parking_status'),
    url(r'^gcheckout/','home.views.guest_check_out'),
    url(r'^usercheckout/','home.views.user_check_out'),
    url(r'^usercheckin/','home.views.user_check_in'),
    url(r'^gcheckin/','home.views.guest_check_in'),
    url(r'^pricing/', 'home.views.pricing'),
    url(r'^enforcement/','home.views.enforcement'),
    url(r'^check/','home.returnlp.check'),
    url(r'^checkuser/','qtmessage.views.check_user'),
    url(r'^gettrigger/','qtmessage.views.get_time_trigger'),
    url(r'^settrigger/','qtmessage.views.set_time_trigger'),
    url(r'^getloc/','qtmessage.views.get_loc_trigger'),
    url(r'^setloc/','qtmessage.views.set_loc_trigger'),
    url(r'^newexperiment/','qtmessage.views.create_experiment'),
    url(r'^clearexperiment/','qtmessage.views.clear_experiment'),
    url(r'^gettime/','qt.views.get_time_trigger'),
    url(r'^settime/','qt.views.set_time_trigger'),
    url(r'^getmessages/','qt.views.get_messages'),
    url(r'^setforms/','qt.views.set_available_forms'),
    url(r'^getforms/','qt.views.get_available_forms'),

    url(r'^ucheckin/','dummyAPIs.views.ucheckin'),
    url(r'^ucheckout/','dummyAPIs.views.ucheckout'),
    url(r'^getrate/','dummyAPIs.views.getrate'),
    url(r'^changelp/','dummyAPIs.views.changelp'),
    url(r'^changebilling/','dummyAPIs.views.changebilling'),
    url(r'^verifyuser/','dummyAPIs.views.verifyuser'),
    url(r'^ulogin','dummyAPIs.views.ulogin'),
    url(r'^uprofile','dummyAPIs.views.uprofile'),
    url(r'^usignin','dummyAPIs.views.usignin'),
    url(r'^uhistory','dummyAPIs.views.parkinghistory'),
    url(r'^receipt','dummyAPIs.views.ureceipt'),
    url(r'^ugetfav','dummyAPIs.views.ugetfavandtokenandstatus'),
    url(r'^uupdatefav','dummyAPIs.views.uupdatefav'),
    url(r'^uregistration','dummyAPIs.views.uregistration'),
    url(r'^uverifyreg','dummyAPIs.views.uverifyreg'),
)

urlpatterns += staticfiles_urlpatterns()
