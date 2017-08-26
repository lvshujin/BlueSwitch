import django_excel as excel
import pyexcel.ext.xls
import pyexcel.ext.xlsx
from django.db.models import Q
from django.shortcuts import get_object_or_404, render, HttpResponse, render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect
from rest_framework import viewsets, generics, permissions, mixins, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from push_notifications.models import GCMDevice

from blueswitch.apps.baidu.models import BaiduDevice

from blueswitch.apps.devices.models import Device, TwinDevice
from blueswitch.apps.toggles.models import ToggleHistory
from blueswitch.apps.devices.serializers import DeviceSerializer, TwinDeviceSerializer
from blueswitch.apps.devices.forms import UploadFileForm


class BLEDeviceViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    **POST DATA**

        {
            "name": "TestDevice",
            "address": "25:50:60:32",
        }

    """
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [permissions.IsAuthenticated,]
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter)
    filter_fields = ('address',)
    search_fields = ('name', 'address',)

    def get_queryset(self, *args, **kwargs):
        queryset = super(BLEDeviceViewSet, self).get_queryset(*args, **kwargs)
        queryset = queryset.filter(user=self.request.user)
        return queryset.distinct()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class BLEDeviceColorView(APIView):
    """
    **POST DATA**

        {
            "address":
                [
                    "25:50:60:32",
                    "25:50:60:33",
                    "25:50:60:34"
                ]
        }
    """
    permission_classes = [permissions.IsAuthenticated,]
    allowed_methods = ['POST']

    def post(self, request, *args, **kwargs):
        address_list = request.data.get('address', None)
        if not address_list:
            return Response({'detail': 'address is required'}, status=status.HTTP_400_BAD_REQUEST)

        new_address_list = list()
        result_list = list()
        for address in address_list:
            new_address_list.append(address.replace(':', ' '))

        for address in new_address_list:
            response = dict()
            msg = ''
            twin_device = TwinDevice.objects.filter(Q(mac1=address) | Q(mac2=address)).values('mac1', 'mac2', 'color').first()
            if twin_device:
                if address == twin_device['mac1']:
                    twin_address = twin_device['mac2']
                else:
                    twin_address = twin_device['mac1']
                try:
                    device = Device.objects.get(address=address)
                    if not (device.user == request.user):
                        msg = 'BLE already paired to user %s' %(device.user.username)

                except Device.DoesNotExist as e:
                    device = Device.objects.filter(address=twin_address).first()
                    if device:
                        if (device.user == request.user):
                            msg = 'Twin BLE is already paired to this user.'

                response.update(message=msg)
                response.update(address=address.replace(' ', ':'))
                response.update(color=twin_device['color'])
                result_list.append(response)

        return Response({'results': result_list}, status=status.HTTP_200_OK)


class RegisterDevice(APIView):
    """
    **POST DATA**

        {
            "address": "25:50:60:32"
        }
    """
    permission_classes = [permissions.IsAuthenticated,]
    def post(self, request, *args, **kwargs):
        address = request.data.get('address', None)
        if not address:
            return Response({'detail': 'address is required.'}, status=status.HTTP_400_BAD_REQUEST)
        address = address.replace(':', ' ')
        device, created = Device.objects.get_or_create(address=address, defaults={'user': request.user, 'name': 'Blueswitch'})
        if not created:
            device.user = request.user
            device.save()

        return Response({'detail': 'Device successfully registered.'}, status=status.HTTP_200_OK)


class DeleteDevice(APIView):
    """
    **POST DATA**

        {
            "address": "25:50:60:32"
        }
    """
    permission_classes = [permissions.IsAuthenticated,]
    def post(self, request, *args, **kwargs):
        address = request.data.get('address', None)
        if not address:
            return Response({'detail': 'address is required.'}, status=status.HTTP_400_BAD_REQUEST)
        address = address.replace(':', ' ')
        Device.objects.filter(address=address).delete()
        ToggleHistory.objects.filter(address=address).delete()
        return Response({'detail': 'Device successfully deleted.'}, status=status.HTTP_200_OK)


class PairedDeviceView(APIView):
    """
    """
    #serializer_class = DeviceSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def get(self, request, *args, **kwargs):
        device_list = Device.objects.filter(user=request.user)
        device_address_list = list(device_list.values_list('address', flat=True))
        response_data_list = list()

        # twin_device = TwinDevice.objects.filter(Q(mac1__in=device_address_list) | Q(mac2__in=device_address_list)).distinct()
        # twin_data = TwinDeviceSerializer(twin_device, many=True, context={'request': request}).data

        for address in device_address_list:
            twin_device = TwinDevice.objects.filter(Q(mac1=address) | Q(mac2=address)).first()

            if twin_device:
                if address == twin_device.mac1:
                    twin_address = twin_device.mac2
                else:
                    twin_address = twin_device.mac1
                try:
                    twin = Device.objects.get(address=twin_address)
                    response_data = DeviceSerializer(twin, context={'request': request}).data
                    if GCMDevice.objects.filter(user=twin.user).exists():
                        response_data.update({'username':twin.user.username})
                    elif BaiduDevice.objects.filter(user=twin.user).exists():
                        response_data.update({'username':twin.user.username})      
                    else:
                        response_data.update({'username': ""})
                    response_data.update(color=twin_device.color)
                    response_data.update(address=twin_address.replace(' ', ':'))
                    response_data.update(twin_address=address.replace(' ', ':'))

                except Device.DoesNotExist as e:
                    response_data = {'url': '', 'name': 'Blueswitch', 'address': twin_address.replace(' ', ':'), 'color': twin_device.color, 'username': '', 'twin_address': address.replace(' ', ':')}
                response_data_list.append(response_data)

        return Response(response_data_list)


@login_required
def upload(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            request.FILES['file'].save_to_database(
                model=TwinDevice,
                mapdict=['mac1', 'mac2', 'color'])
            return HttpResponseRedirect('/')
    else:
        form = UploadFileForm()
    return render_to_response('devices/upload_file.html', {'form': form}, context_instance=RequestContext(request))
