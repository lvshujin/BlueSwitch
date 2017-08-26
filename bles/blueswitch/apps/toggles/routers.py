from django.conf.urls import patterns, include, url
from rest_framework.routers import SimpleRouter

from blueswitch.apps.toggles import views

router = SimpleRouter()

urlpatterns = patterns('',
    url(r'^toggle/device/$', views.ToggleDeviceView.as_view(), name='toggle-device'),
    url(r'^toggle/history/$', views.ToggleHistoryView.as_view(), name='toggle-history'),
    url(r'^toggle/history/clear/$', views.ToggleHistoryClearView.as_view(), name='clear-toggle-history'),
)

urlpatterns += router.urls
