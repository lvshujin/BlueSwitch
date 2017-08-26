from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from blueswitch.apps.devices.models import Device


class ToggleHistory(models.Model):
    """
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='toggle_historys')
    address = models.CharField('mac address', max_length=255)
    toggled_at = models.DateTimeField(auto_now=True)


class ToggleTransaction(models.Model):
    """
    """
    STATUS_CHOICES = (
        ('pending', "Pending"),
        ('success', "Success"),
        ('failed', "Failed"),
    )

    device = models.ForeignKey(Device)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    transaction_at = models.DateTimeField(auto_now=True)
