import re
from django.db.models import Q
from push_notifications.models import APNSDevice, GCMDevice
from rest_framework import serializers
from rest_framework.reverse import reverse

from blueswitch.apps.baidu.models import BaiduDevice

from django.contrib.auth import get_user_model
User = get_user_model()


class UserRegistrationSerializer(serializers.HyperlinkedModelSerializer):
    """
    """

    class Meta:
        model = User
        fields = ('name', 'username', 'email', 'password',)
        write_only_fields = ('password',)

    def validate_email(self, value):
        """
        Check the uniqueness of the email.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email already exists")
        return value

    def validate_username(self, value):
        """
        Check the uniqueness of the username.
        """
        if len(value)<6 or len(value)>30:
            raise serializers.ValidationError("Username should be between 6 to 30 characters.")
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("User with this username already exists")
        if not (re.match('^[a-zA-Z0-9]*$',value)):
            raise serializers.ValidationError("Only characters are allowed.")
        return value


    def validate_password(self, value):
        """
        Check the uniqueness of the password.
        """
        if len(value)<6 or len(value)>30:
            raise serializers.ValidationError("Password should be between 6 to 30 characters.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = User.objects.create(**validated_data)
        instance.set_password(password)
        instance.save()
        return instance


class MeSerializer(serializers.HyperlinkedModelSerializer):
    """
    """

    class Meta:
        model = User
        fields = ('name', 'username', 'email')

    def validate_email(self, value):
        """
        Check the uniqueness of the email.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email already exists")
        return value


class ForgotPasswordSerializer(serializers.HyperlinkedModelSerializer):
    """
    """
    email = serializers.EmailField(max_length=255, allow_blank=False)
    class Meta:
        model = User
        fields = ("email",)

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User is not registered with this email.")

        return value


class UserDeviceSerializer(serializers.Serializer):
    """
    """
    device_type = serializers.ChoiceField(['android','ios'], required=True, write_only=True)
    device_id = serializers.CharField()
    registration_id = serializers.CharField()


    def create(self, validated_data):
        """
        """
        device_type = validated_data.pop('device_type', 'android')
        if device_type == 'ios':
            return APNSDevice.objects.create(**validated_data)

        return GCMDevice.objects.create(**validated_data)

class UserBaiduDeviceSerializer(serializers.Serializer):
    """
    """
 
    device_id = serializers.CharField()
    buser_id = serializers.CharField()
    bchannel_id = serializers.CharField()
    
    def create(self, validated_data):
        """
        """        
        return BaiduDevice.objects.create(**validated_data)
