from django.conf.urls import url
from blueswitch.apps.devices import views


urlpatterns = [
    url(r'^upload-file/$', views.upload, name='file-upload'),
]
