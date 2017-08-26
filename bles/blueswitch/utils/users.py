import json
import urllib
from rest_framework import status
from rest_framework.response import Response

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from django.contrib.auth import get_user_model
User = get_user_model()


def get_facebook_user(token):
    """
    Authenticates user from facebook using user access token. And gets or creates user then returns app user.

    """


    http_request = urllib.request.Request("https://graph.facebook.com/v2.1/me/?fields=id,first_name,last_name,email,picture&access_token=%s" % (token, ), method='GET')

    try:
        json_response = urllib.request.urlopen(http_request).read()
    except urllib.error.HTTPError:
        return None

    response = json.loads(json_response.decode())

    first_name = response.pop('first_name')
    last_name = response.pop('last_name')
    email = response.pop('email', None)
    picture = response.pop('picture', None)
    name = '{0} {1}'.format(first_name, last_name)

    if email is None:
        return Response({'detail': 'Access Token has missing email scope.'}, status=status.HTTP_400_BAD_REQUEST)
    facebook_uid = response.pop('id')
    username = '%s%s' %(name, facebook_uid)
    response.update({'facebook_uid':facebook_uid, 'name': name, 'username': username})

    user, created = User.objects.get_or_create(email=email, defaults=response)
    # if picture:
    #     image_url = picture.get('data').get('url', None)
    #     img_temp = NamedTemporaryFile(delete=True)
    #     img_temp.write(urllib.request.urlopen(image_url).read())
    #     img_temp.flush()
    #     user.profile_picture.save('%s_%d.jpg' %(user.name,user.id), File(img_temp))

    return user
