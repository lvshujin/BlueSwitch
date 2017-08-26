from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

from blueswitch.libs.accounts.views import login_view, logout_view

admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'blueswitch.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^api/v1/', include('blueswitch.routers', namespace='v1')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', login_view, name='login'),
    url(r'^accounts/logout/$', logout_view, name='logout'),

    #url(r'^', include('blueswitch.libs.accounts.urls')),
    url(r'^', include('blueswitch.apps.users.urls')),
    url(r'^', include('blueswitch.apps.devices.urls')),
)


# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns += patterns('',
#         url(r'^__debug__/', include(debug_toolbar.urls)),
#     ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
