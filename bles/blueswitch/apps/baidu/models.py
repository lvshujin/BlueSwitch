from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from .fields import HexIntegerField


class BDevice(models.Model):
	name = models.CharField(max_length=255, verbose_name=_("Name"), blank=True, null=True)
	active = models.BooleanField(verbose_name=_("Is active"), default=True,
		help_text=_("Inactive devices will not be sent notifications"))
	user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
	date_created = models.DateTimeField(verbose_name=_("Creation date"), auto_now_add=True, null=True)

	class Meta:
		abstract = True

	def __unicode__(self):
		return self.name or \
			str(self.device_id or "") or \
			"%s for %s" % (self.__class__.__name__, self.user or "unknown user")










		






			


class BaiduDevice(BDevice):	
	device_id = HexIntegerField(verbose_name=_("Device ID"), blank=True, null=True, db_index=True,
		help_text=_("android device id (always as hex)"))
	buser_id = models.TextField(verbose_name=_("Baidu User ID"))
	bchannel_id = models.TextField(verbose_name=_("Baidu Channel ID"))



	class Meta:
		verbose_name = _("Baidu device")







	


		
