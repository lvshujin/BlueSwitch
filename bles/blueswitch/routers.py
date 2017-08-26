from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'blueswitch.views.api_root', name='api_root'),
    #url(r'^', include('blueswitch.libs.accounts.routers')),
    url(r'^', include('blueswitch.apps.devices.routers')),
    url(r'^', include('blueswitch.apps.toggles.routers')),
    url(r'^', include('blueswitch.apps.users.routers')),
    url(r'^', include('blueswitch.apps.me.routers')),
)
