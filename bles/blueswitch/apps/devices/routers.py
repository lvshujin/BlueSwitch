from django.conf.urls import patterns, include, url
from rest_framework.routers import SimpleRouter

from blueswitch.apps.devices import views

router = SimpleRouter()
#router.register(r'devices', views.BLEDeviceViewSet, base_name='device')

urlpatterns = patterns('',
    url(r'^device/color/$', views.BLEDeviceColorView.as_view(), name='device-color'),
    url(r'^devices/$', views.PairedDeviceView.as_view(), name='paired-device'),
    url(r'^register/device/$', views.RegisterDevice.as_view(), name='register-userdevice'),
    url(r'^delete/device/$', views.DeleteDevice.as_view(), name='delete-userdevice'),
)

urlpatterns += router.urls
