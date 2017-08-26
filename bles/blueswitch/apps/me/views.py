import re
from django.contrib import auth
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.contrib.auth import get_user_model
User = get_user_model()


class ChangeUsernameView(APIView):
    """
    **POST DATA**

        {"username": "admin"}
    """
    permission_classes = [IsAuthenticated,]
    allowed_methods = ['POST']

    def post(self, request, *args, **kwargs):
        try:
            username = request.data['username']
        except KeyError:
            return Response({'detail': 'username is required'}, status=status.HTTP_400_BAD_REQUEST)

        if len(username)<6 or len(username)>30:
            return Response({'detail': "Username should be between 6 to 30 characters."}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return Response({'detail': "User with this username already exists"}, status=status.HTTP_400_BAD_REQUEST)
        if not (re.match('^[a-zA-Z0-9]*$',username)):
            return Response({'detail': "Only characters are allowed."}, status=status.HTTP_400_BAD_REQUEST)

        request.user.username = username
        request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChangePasswordView(APIView):
    """
    **POST DATA**

        {"new_password": "1234567", "current_password": "123456"}
    """
    permission_classes = [IsAuthenticated,]
    allowed_methods = ['POST']

    def post(self, request, *args, **kwargs):
        try:
            password = request.data['new_password']
            current_password = request.data['current_password']
        except KeyError:
            return Response({'detail': 'new_password & current_password both are required'}, status=status.HTTP_400_BAD_REQUEST)

        if not request.user.check_password(current_password):
            return Response({'detail': "current_password is invalid. Please enter a valid current_password"}, status=status.HTTP_400_BAD_REQUEST)

        if len(password)<6 or len(password)>30:
            return Response({'detail': "new_assword should be between 6 to 30 characters."}, status=status.HTTP_400_BAD_REQUEST)

        request.user.set_password(password)
        request.user.save()

        auth.update_session_auth_hash(request, request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)
