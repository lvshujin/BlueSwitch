from django.db.models import Q

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from blueswitch.apps.devices.models import TwinDevice, Device
from blueswitch.apps.toggles.models import ToggleHistory
from blueswitch.apps.devices import tasks


class ToggleDeviceView(APIView):
    """
    **POST DATA**

        {"address": "12:30:56:23"}

    """
    permission_classes = [IsAuthenticated,]
    allowed_methods = ['POST']

    def post(self, request, *args, **kwargs):
        try:
            address = request.data['address']
        except KeyError:
            return Response({'detail': 'address is required'}, status=status.HTTP_400_BAD_REQUEST)

        address = address.replace(':', ' ')
        twin_device = TwinDevice.objects.filter(Q(mac1=address) | Q(mac2=address))
        if len(twin_device):
            if address == twin_device.first().mac1:
                twin_address = twin_device.first().mac2
            else:
                twin_address = twin_device.first().mac1

            try:
                device = Device.objects.get(address=twin_address)
                notify_user = device.user
                tasks.send_toggle_notification(request.user, device, twin_address)

                return Response(status=status.HTTP_204_NO_CONTENT)

            except Device.DoesNotExist:
                return Response({'detail': 'device with this address does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        #return Response({'detail': 'No twin device for this device'}, status=status.HTTP_400_BAD_REQUEST)
        #tasks.send_toggle_notification(request.user, device)
        return Response({'detail': 'No twin table exists with this device'}, status=status.HTTP_400_BAD_REQUEST)


class ToggleHistoryView(APIView):
    """
    **POST DATA**

        {"address": "12:30:56:23"}

    """
    permission_classes = [IsAuthenticated,]
    allowed_methods = ['POST']

    def post(self, request, *args, **kwargs):
        try:
            address = request.data['address']
        except KeyError as e:
            return Response({'detail': 'address is required'}, status=status.HTTP_400_BAD_REQUEST)

        address = address.replace(':', ' ')
        response = ToggleHistory.objects.filter(address=address).values('user__username', 'toggled_at')
        return Response({'results': response}, status=status.HTTP_200_OK)


class ToggleHistoryClearView(APIView):
    """
    **POST DATA**

        {"address": "12:30:56:23"}

    """
    def post(self, request, *args, **kwargs):
        try:
            address = request.data['address']
        except KeyError as e:
            return Response({'detail': 'address is required'}, status=status.HTTP_400_BAD_REQUEST)

        address = address.replace(':', ' ')
        ToggleHistory.objects.filter(address=address).delete()
        return Response({'detail': 'Toggle History cleared successfully.'}, status=status.HTTP_200_OK)
