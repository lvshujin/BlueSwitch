import uuid
import json

from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.views.generic import View, TemplateView, UpdateView, DetailView, CreateView
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import user_passes_test, login_required
from django.template.loader import render_to_string

from rest_framework import status, views, generics, viewsets, permissions, filters
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.decorators import api_view, detail_route
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.views import APIView
from rest_framework.reverse import reverse
from push_notifications.models import APNSDevice, GCMDevice

from blueswitch.apps.baidu.models import BaiduDevice

from blueswitch.libs.accounts.models import TempToken
from blueswitch.apps.users.serializers import UserRegistrationSerializer, MeSerializer, ForgotPasswordSerializer, UserDeviceSerializer, UserBaiduDeviceSerializer
from blueswitch.apps.users import tasks as email_tasks
from blueswitch.mixins.datatable import DatatableSearchMixin
from blueswitch.apps.users.permissions import AdminPermissionMixin
from blueswitch.apps.devices.models import TwinDevice
from blueswitch.apps.users.forms import DeviceUpdateForm, ProfileForm
from blueswitch.utils.users import get_facebook_user

from django.contrib.auth import get_user_model
User = get_user_model()


class UserRegistrationView(generics.CreateAPIView):
    """
    Register a new user.

    **POST DATA**

        {
            "name": "Gopal Roy",
            "username": "gopal",
            "email": "gopal.roy@finoit.com",
            "password": "123456"
        }

    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)

        response = MeSerializer(user, context={'request': request}).data
        response.update({'token': token.key})

        return Response(response)


@api_view(('POST',))
def sign_in_with_facebook(request):
    """
    **POST Data**

        {"access_token": "2gh234h234g657jkk5"}

    **Access token scope**

        id
        first-name
        last-name
        picture-url
        email-address
    """

    access_token = request.data.get('access_token', None)

    if access_token is None or access_token == '':
        return Response({"access_token": "This field is required."}, status=status.HTTP_400_BAD_REQUEST)

    user = get_facebook_user(access_token)
    if isinstance(user, Response):
        return user
    elif user is not None:
        token, created = Token.objects.get_or_create(user=user)
        response = UserRegistrationSerializer(user, context={'request': request}).data
        response.update({'token': token.key})
        response.pop('password', None)
        return Response(response)
    else:
        return Response({"detail" : "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)


class ObtainAuthToken(views.APIView):
    """
    **POST DATA**

        {
            "username": "gopal",
            "password": "123456"
        }

    """
    throttle_classes = ()
    serializer_class = AuthTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        GCMDevice.objects.filter(user=user).delete()
        BaiduDevice.objects.filter(user=user).delete()
        Token.objects.filter(user=user).delete()
        token = Token.objects.create(user=user)
        result = MeSerializer(user, context={'request': request}).data
        result.update({'token': token.key})

        return Response(result)


class PasswordReset(APIView):
    """
    **POST DATA**

        {"email": "test@email.com"}
    """
    permission_classes = [permissions.AllowAny, ]

    def post(self, request, format=None):
        """
        """
        serializer = ForgotPasswordSerializer(data=request.data, context={'request': request})

        serializer.is_valid(raise_exception=True)
        user = User.objects.get(email=serializer.validated_data['email'])

        token = uuid.uuid1().hex
        TempToken.objects.create(user=user, token=token)
        password_reset_link = reverse('password-reset-confirm', kwargs={"token": token}, request=request)
        email_tasks.email_password_reset_link(user, password_reset_link)

        return Response(status=status.HTTP_204_NO_CONTENT)


def password_reset_confirm(request, token):
    """
    """
    user_email = get_object_or_404(TempToken, token=token)
    template_name = 'accounts/reset_password.html'

    if request.method == "POST":
        user_email = get_object_or_404(TempToken, token=token)

        password1 = request.POST.get('password', None)
        password2 = request.POST.get('confirm_password', None)

        if not password1 and password2:
            return render(request, template_name, {'error': 'Password is required.'})
        elif password1 != password2:
            return render(request, template_name, {'error': 'Confirm password didn\'t match.'})

        if user_email.created_at is not None:
            return render(request, template_name, {'error': 'This link has been expired.'})

        user = user_email.user
        user.set_password(password1)
        user.save()
        user_email.created_at = timezone.now()
        user_email.save()
        return render(request, 'accounts/reset_password_confirm.html')

    return render(request, template_name)


class BLEDeviceList(AdminPermissionMixin, TemplateView):
    """
    """
    template_name = 'devices/device_list.html'

    def get_context_data(self, **kwargs):
        """
        Preparing the Context Variable required in the template rendering.
        """
        context = super(BLEDeviceList, self).get_context_data(**kwargs)
        datatable_headers = [
            {'mData': 'mac1', 'sTitle': 'BLE1', 'sWidth': '10%', },
            {'mData': 'mac2', 'sTitle': 'BLE2', 'sWidth': '10%', },
            {'mData': 'color', 'sTitle': 'Color', 'sWidth': '5%', },
            {'mData':'actions', 'sTitle':'Action', 'sWidth':'10%', 'bSortable': False},
        ]
        context['datatable_headers'] = json.dumps(datatable_headers)
        return context


class BLEDeviceListingTable(AdminPermissionMixin, DatatableSearchMixin, BaseDatatableView):
    """
    """
    model = TwinDevice
    columns = ['mac1', 'mac2', 'color']
    order_columns = ['mac1', 'mac2', 'color']
    search_columns = ['mac1', 'mac2', 'color']

    def get_initial_queryset(self):
        queryset = super(BLEDeviceListingTable, self).get_initial_queryset()
        return queryset.values(*self.columns + ['id'])

    def prepare_results(self, qs):
        """
        Preparing the final result after fetching from the data base to render on the data table.

        :param qs:
        :return qs
        """
        json_data = [ { key: val if val else "" for key, val in dct.items() } for dct in qs ]
        for dct in json_data:
            print(dct['color'])
            dct.update(actions='<a href="/devices/{0}/edit/" class="btn default btn-xs purple">'
                '<i class="fa fa-edit"></i> Edit </a>&nbsp&nbsp'
                '<a class="btn default btn-xs" data-toggle="modal" onclick="javascript:delete_device({0})">'
                '<i class="fa fa-trash-o"></i> Delete </a>'.format(dct['id'])
            )
            dct.update(mac1='<a href="/devices/{0}/">{1}</a>'.format(dct['id'], dct['mac1']))
            dct.update(mac2='<a href="/devices/{0}/">{1}</a>'.format(dct['id'], dct['mac2']))
            dct.update(color=dct['color'].title())
        return json_data


@login_required
@user_passes_test(lambda u: u.is_admin)
def device_delete(request, pk):
    device = TwinDevice.objects.filter(pk=pk)
    device.delete()
    return HttpResponse(json.dumps({'status': True}))


class BLEDeviceDetail(AdminPermissionMixin, DetailView):
    """
    Class Based View to render the Devices Details

    """
    model = TwinDevice
    template_name = 'devices/device_detail.html'


class DeviceUpdate(AdminPermissionMixin, UpdateView):
    """
    Class Based View to Update a Device.
    """
    template_name = 'devices/device_edit.html'
    model = TwinDevice
    form_class = DeviceUpdateForm
    success_url = '/'


class ProfileUpdate(AdminPermissionMixin, UpdateView):
    """
    """
    model = User
    form_class = ProfileForm
    template_name = 'accounts/profile.html'
    success_url = '/'

    def get_object(self, *args, **kwargs):
        return self.request.user


    def form_valid(self, form):
        """
        Called if all forms are valid. Creates a Recipe instance along with
        associated Ingredients and Instructions and then redirects to a
        success page.
        """
        password = form.cleaned_data.pop('password1')
        self.object = form.save(commit=False)
        if password != "":
            self.object.set_password(password)
        self.object.save()
        return HttpResponseRedirect(self.success_url)


class UserDeviceView(generics.CreateAPIView):
    """
    Register ios/android device for push notifications.
    """
    serializer_class = UserDeviceSerializer
    permission_classes = [permissions.IsAuthenticated ]

    def post(self, request, format=None):
        """
        Add requesting user (customer) as device owner for Device.

        Delete device if already exists with this registration_id.
        """
        serializer = self.serializer_class(data=request.data, context={'request': request})

        if serializer.is_valid():
            registration_id = serializer.validated_data.get('registration_id')
            device_type = serializer.validated_data.get('device_type')
            if device_type == 'ios':
                devices = APNSDevice.objects.filter(Q(registration_id=registration_id) | Q(user=self.request.user))
            elif device_type == 'android':
                devices = GCMDevice.objects.filter(Q(registration_id=registration_id) | Q(user=self.request.user))
 
            
            if devices.exists():
                devices.delete()
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserBaiduDeviceView(generics.CreateAPIView):
    """
    Register android-baidu device for push notifications.
    """
    serializer_class = UserBaiduDeviceSerializer
    permission_classes = [permissions.IsAuthenticated ]

    def post(self, request, format=None):        
        serializerB = self.serializer_class(data=request.data, context={'request': request})

        if serializerB.is_valid():
            buser_id = serializerB.validated_data.get('buser_id')            
            
  
            devices = BaiduDevice.objects.filter(Q(buser_id=buser_id) | Q(user=self.request.user))
            if devices.exists():
                devices.delete()
            serializerB.save(user=self.request.user)
            return Response(serializerB.data, status=status.HTTP_201_CREATED)
        return Response(serializerB.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteDeviceView(APIView):
    """
    Delete the device of user when user logs out.

    **POST DATA**

        {
            "device_id": "FGHEE6557213",
            "device_type": "android"
        }
    """
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        """
        """
        device_id = request.data.get('device_id', None)
        device_type = request.data.get('device_type', None)
        if not device_id:
            return Response({'detail': 'device_id is required.'}, status=status.HTTP_400_BAD_REQUEST)

        if device_type == 'android':
            try:
                GCMDevice.objects.filter(device_id=device_id).delete()
            except Exception as e:
                pass
        if device_type == 'android-baidu':
            try:
               BaiduDevice.objects.filter(device_id=device_id).delete()
            except Exception as e:
                pass

        if device_type == 'ios':
            try:
                APNSDevice.objects.filter(device_id=device_id).delete()
            except Exception as e:
                pass

        return Response(status=status.HTTP_204_NO_CONTENT)


class DeviceCreate(AdminPermissionMixin, CreateView):
    """
    """
    model = TwinDevice
    template_name = 'devices/device_add.html'
    form_class = DeviceUpdateForm
    success_url = '/devices/'
