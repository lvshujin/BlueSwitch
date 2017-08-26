from rest_framework import serializers

from blueswitch.apps.devices.models import Device, TwinDevice


class NestedDeviceSerializer(serializers.HyperlinkedModelSerializer):
    """
    """
    class Meta:
        model = Device
        exclude = ('user', )


class DeviceSerializer(serializers.HyperlinkedModelSerializer):
    """
    """
    class Meta:
        model = Device
        exclude = ('user', )
        read_only_fields = ('color', )


class TwinDeviceSerializer(serializers.ModelSerializer):
    """
    """
    class Meta:
        model = TwinDevice
        exclude = ('id', 'paired_at',)
