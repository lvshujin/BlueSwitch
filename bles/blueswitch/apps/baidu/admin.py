from django.contrib import admin
from .models import BaiduDevice

class BDeviceAdmin(admin.ModelAdmin):
	list_display = ("__unicode__", "device_id","buser_id", "bchannel_id", "user", "active", "date_created")
	
admin.site.register(BaiduDevice, BDeviceAdmin)
