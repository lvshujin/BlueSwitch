from django.contrib import admin
from blueswitch.apps.devices.models import Device, TwinDevice

admin.site.register(Device)
admin.site.register(TwinDevice)
