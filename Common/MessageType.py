from enum import Enum


class MessageType(Enum):

    PERSONAL_INIT_INIT = '1'
    PERSONAL_INIT_OK = '2'

    PERSONAL_ONLINE_INIT = '3'
    PERSONAL_ONLINE_OK = '4'

    DEVICE_INIT_INIT = '5'
    DEVICE_INIT_START = '6'
    DEVICE_INIT_OK_TO_PERSONAL = '7'
    DEVICE_INIT_OK_TO_DEVICE = '8'
    DEVICE_INIT_CONNECT_TO_PERSONAL = '9'
    DEVICE_INIT_OK = '10'

    DEVICE_ONLINE_INIT = '11'
    DEVICE_ONLINE_GLOBAL_RETURN = '12'
    DEVICE_ONLINE_CONNECT = '13'
