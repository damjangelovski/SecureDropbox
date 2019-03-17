from enum import Enum


class MessageType(Enum):

    PERSONAL_INIT_INIT = 'personal-init-init'
    PERSONAL_INIT_OK = 'personal-init-ok'

    PERSONAL_ONLINE_INIT = 'personal-online-init'
    PERSONAL_ONLINE_OK = 'personal-online-ok'

    DEVICE_INIT_INIT = 'device-init-init'
    DEVICE_INIT_INIT_OK = 'device-init-init-ok'
    DEVICE_INIT_START = 'device-init-start'
    DEVICE_INIT_OK_TO_PERSONAL = 'device-init-ok-to-personal'
    DEVICE_INIT_OK_TO_DEVICE = 'device-init-ok-to-device'
    DEVICE_INIT_CONNECT_TO_PERSONAL = 'device-init-connect-to-personal'
    DEVICE_INIT_OK = 'device-init-ok'

    DEVICE_ONLINE_INIT = 'device-online-init'
    DEVICE_ONLINE_GLOBAL_RETURN = 'device-online-global-return'
    DEVICE_ONLINE_CONNECT = 'device-online-connect'
    DEVICE_ONLINE_OK = 'device-online-ok'

    SYNC_CHECK = 'sync-check'
    SYNC_CHECK_OK = 'sync-check-ok'
    SYNC_REQUEST = 'sync-request'
    SYNC_REQUEST_OK = 'sync-request-ok'
