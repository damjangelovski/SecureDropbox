from enum import Enum


class MessageProperty(Enum):

    MESSAGE_TYPE = 'message-type'
    USERNAME = 'username'
    PERSONAL_PUBLIC_KEY = 'personal-public-key'
    STATUS = 'status'
    PERSONAL_IP_SOCKET = 'personal-ip-socket'
    ONE_TIME_PAD = 'one-time-pad'
    DEVICE_PUBLIC_KEY = 'device-public-key'
    DEVICE_ID = 'device-id'


