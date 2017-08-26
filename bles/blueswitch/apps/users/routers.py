from django.conf.urls import url, patterns
from rest_framework.routers import SimpleRouter

from blueswitch.apps.users import views as api_views

router = SimpleRouter()
#router.register(r'users', api_views.UserViewSet, base_name='user')

urlpatterns = patterns('',
    url(r'^register/$', api_views.UserRegistrationView.as_view(), name='register'),
    url(r'^api-token-auth/', api_views.ObtainAuthToken.as_view(), name='api-token-auth'),
    url(r'^login/facebook/$', api_views.sign_in_with_facebook, name='facebook-sign-in'),
    url(r'^users/device/$', api_views.UserDeviceView.as_view(), name='user-device'),
    url(r'^users/baidu_device/$', api_views.UserBaiduDeviceView.as_view(), name='user-baidu-device'),
    url(r'^users/device/delete/$', api_views.DeleteDeviceView.as_view(), name='delete-device'),
    url(r'^password/reset/$', api_views.PasswordReset.as_view(), name='password-reset'),
)

urlpatterns += router.urls
