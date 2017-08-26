from collections import OrderedDict
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

@api_view(['GET'])
def api_root(request, format=None):
    """
    Each API Endpoint contains corresponding documentation.
    """

    return Response(OrderedDict([
        ('Registration', OrderedDict([
            ('Login', reverse('api-token-auth', request=request, format=format)),
            ('Register', reverse('register', request=request, format=format)),
            ('Forgot-Password' , reverse('password-reset', request=request, format=format)),
            ('Sign in with Facebook' , reverse('facebook-sign-in', request=request, format=format)),
            ('Register User Device' , reverse('user-device', request=request, format=format)),
            ('Register User Baidu Device' , reverse('user-baidu-device', request=request, format=format)),
            ('Delete User Device' , reverse('delete-device', request=request, format=format)),

        ])),

        ('Me', OrderedDict([
            ('Change Username', reverse('change-username', request=request, format=format)),
            ('Change Password', reverse('change-password', request=request, format=format)),
        ])),

        ('Device', OrderedDict([
            ('Paired Device', reverse('paired-device', request=request, format=format)),
            ('Register Device' , reverse('register-userdevice', request=request, format=format)),
            ('Delete Device' , reverse('delete-userdevice', request=request, format=format)),
            ('Device Color', reverse('device-color', request=request, format=format)),
        ])),

        ('Toggle', OrderedDict([
            ('Toggle Device', reverse('toggle-device', request=request, format=format)),
            ('Toggle History', reverse('toggle-history', request=request, format=format)),
            ('Clear Toggle History', reverse('clear-toggle-history', request=request, format=format)),
        ])),

    ]))
