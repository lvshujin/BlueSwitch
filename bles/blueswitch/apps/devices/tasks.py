from django.utils import timezone
from django.db.models import Q

from push_notifications.models import GCMDevice
from blueswitch.apps.toggles.models import ToggleHistory
from blueswitch.apps.baidu.models import BaiduDevice

from baidupush import BaiduPush

import random
from time import sleep

apikey = "g3jCgx5YdcZHUAqu67NpVanH" #"haas7q0WQHzFaV0ifHWVLy86"
secretkey = "OgYnRbXpG3GlTo1HE2Cwz9tuKLTBzRMp" #"hv976MGWGrDMpz1QbO8jQvPS1aKYk5zc"

#testuser_id = "694022595129931823"
#testchannel_id = 3627045918107601314

#testmessage = "abcde" #{"BAIDU": "{\"title\":\"killer\",\"description\":\"killer\"}"}#"{'title':'baidu push','description':'anaconda'}"
message_key = "key1"

def send_toggle_notification(user, device, address):
    """
    """
    message1 = "Your device is toggled.(GCM)"
    message2 = "Your device is toggled.(Baidu)"
    
    numb = random.randint(100,10000)
    ToggleHistory.objects.create(user=user, address=address)
    dev_usr = device.user
    gcm_devices = GCMDevice.objects.filter(user=dev_usr)
    gcm_devices.send_message(message=message1, extra={"address": device.address.replace(' ', ':'), "username": user.username, "numb": str(numb)})

    bdu_devices = BaiduDevice.objects.filter(user=dev_usr).values('buser_id','bchannel_id').first()    
    #bdu_devices.send_message(message=message2, extra={"address": device.address.replace(' ', ':'), "username": user.username})
 
    if not  bdu_devices:
    	return  
    c = BaiduPush(apikey, secretkey)
    push_type = BaiduPush.PUSH_TO_USER
    optional = dict()
    userID = bdu_devices['buser_id']
    channelID = bdu_devices['bchannel_id']
    optional[BaiduPush.USER_ID] = userID
    optional[BaiduPush.CHANNEL_ID] = channelID
    optional[BaiduPush.MESSAGE_TYPE] = BaiduPush.PUSH_MESSAGE #PUSH_NOTIFICATION
    #optional[BaiduPush.MESSAGE_TYPE] = BaiduPush.PUSH_NOTIFICATION
  
    allmsg = message2 + "%%" + device.address.replace(' ', ':') + "%%" + user.username + "%%" + str(numb)
    #allmsg = "{'title':'baidu push','description':'message from python sdk'}"    
    ret = c.push_msg(push_type, allmsg, message_key, optional)
    sleep(0.3)
    ret = c.push_msg(push_type, allmsg, message_key, optional)
    sleep(0.3)
    ret = c.push_msg(push_type, allmsg, message_key, optional)

