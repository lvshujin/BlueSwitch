
m django.utils import timezone
from django.db.models import Q

from push_notifications.models import GCMDevice
from blueswitch.apps.toggles.models import ToggleHistory
from baidupush import BaiduPush

apikey = "haas7q0WQHzFaV0ifHWVLy86" #"76Yi0ZBGGV2HrAziIiYEFtRh"
secretkey = "hv976MGWGrDMpz1QbO8jQvPS1aKYk5zc"
user_id = "694022595129931823"		#"1105115563847474869"
channel_id = 3627045918107601314	#3944730196422489622

#message = "{'title':'baidu push','description':'message from python sdk'}"
message_key = "key1"

def send_toggle_notification(user, device, address):
    """
    """
    message = "Your device is toggled."

    gcm_devices = GCMDevice.objects.filter(user=device.user)
    gcm_devices.send_message(message=message, extra={"address": device.address.replace(' ', ':'), "username": user.username})


    c = BaiduPush(apikey, secretkey)
    push_type = BaiduPush.PUSH_TO_USER
    optional = dict()
    optional[BaiduPush.USER_ID] = user_id
    optional[BaiduPush.CHANNEL_ID] = channel_id
    optional[BaiduPush.MESSAGE_TYPE] = BaiduPush.PUSH_NOTIFICATION
    ret = c.push_msg(push_type, message=={"address": device.address.replace(' ', ':'), "username": user.username}, message_key, optional)

    ToggleHistory.objects.create(user=user, address=address)

