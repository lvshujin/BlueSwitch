from django.conf.urls import url, patterns

from blueswitch.apps.me import views as api_views


urlpatterns = patterns('',
    #url(r'^me/$', api_views.MeView.as_view(), name='me'),
    url(r'^me/username/change/', api_views.ChangeUsernameView.as_view(), name='change-username'),
    url(r'^me/password/change/', api_views.ChangePasswordView.as_view(), name='change-password'),
)
