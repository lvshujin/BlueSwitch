"""
"""
from django.conf.urls import patterns, url
from django.views.decorators.csrf import csrf_exempt

from blueswitch.apps.users import views


urlpatterns = patterns('',
    url(r'^password/reset/confirm/(?P<token>[\w._-]+)/$', views.password_reset_confirm, name='password-reset-confirm'),
    #url(r'^verify/email/(?P<token>[\w._-]+)/$', views.verify_email_view, name='verify-email'),

    url(r'^$', views.BLEDeviceList.as_view(), name='index'),
    url(r'^devices/$', views.BLEDeviceList.as_view(), name='deviceList'),
    url(r'^devices/Listing/$', views.BLEDeviceListingTable.as_view(), name='BLEDeviceListingTable'),
    url(r'^devices/(?P<pk>\d+)/edit/$', views.DeviceUpdate.as_view(), name='devices-edit'),
    url(r'^devices/(?P<pk>\d+)/delete/$', views.device_delete, name='device-delete'),
    url(r'^devices/new/$', views.DeviceCreate.as_view(), name='devices-add'),
    url(r'^devices/(?P<pk>\d+)/$', views.BLEDeviceDetail.as_view(), name='device-detail'),

    url(r'^profile/$', views.ProfileUpdate.as_view(), name='profile-update'),
)
