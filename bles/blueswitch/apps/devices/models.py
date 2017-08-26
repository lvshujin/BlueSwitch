from django.db import models
from django.utils.translation import ugettext_lazy as _

from blueswitch.libs.accounts.models import User


class Device(models.Model):
    """
    """
    name = models.CharField(_('device name'), max_length=255)
    color = models.CharField(_('color'), max_length=255, null=True, blank=True)
    address = models.CharField('mac address', max_length=255, unique=True)
    user = models.ForeignKey(User, related_name='devices')

    def __str__(self):
        return "%s - %s" %(self.name, self.address)

class TwinDevice(models.Model):
    """
    """
    COLOR_CHOICES = (
        ('yellow', 'Yellow'),
        ('magenta', 'Magenta'),
        ('cyan', 'Cyan'),
        ('red', 'Red'),
        ('green', 'Green'),
        ('blue', 'Blue'),
        ('white', 'White'),
        ('black', 'Black'),
        ('orange', 'Orange'),
        ('pink', 'Pink'),
    )
    mac1 = models.CharField('mac address1', max_length=255)
    mac2 = models.CharField('mac address2', max_length=255)
    color = models.CharField(_('color'), max_length=25, choices=COLOR_CHOICES)
    paired_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s - %s" %(self.mac1, self.mac2)
