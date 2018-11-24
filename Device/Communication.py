import requests
from Common.MessageType import MessageType

globalIP = '127.0.0.1:5000'
personalIP = ''
deviceID = 0

def registerDevice(username, otp):
    req = requests.request('POST', globalIP,
                           data={'messageType': MessageType.DEVICE_INIT_START, 'username': username, 'otp': otp})

    if req.status_code != 200:
        print('can\'t register Device, request status $s'%req.status_code)
        return
    resp = req.json()
    if resp.get('messageType') != MessageType.DEVICE_INIT_OK_TO_DEVICE:
        print('bad message type %d, continuing...'%resp.get('messageType'))

    if 'id' not in resp:
        print('id not included, continuing...')
    else:
        global deviceID
        deviceID = resp.get('id')
        print("id is %d"%deviceID)

    if 'pIP' not in resp:
        print('personal server IP not included, breaking...')
        return
    global personalIP
    personalIP = resp.get('pIP')

    finalOK = requests.request('POST', personalIP,
                               data = {'messageType':MessageType.DEVICE_INIT_CONNECT_TO_PERSONAL, 'username':username,
                                       'otp':otp, 'deviceId':deviceID})

    if finalOK.status_code != 200:
        print('can\'t register Device, request status $s'%req.status_code)
        return
    finalOKr = finalOK.json()
    if finalOKr.get('messageType') != MessageType.DEVICE_INIT_OK:
        print('bad message type %d, continuing...'%finalOKr.get('messageType'))

    if 'status' not in finalOKr:
        print('status not in final ok response')
        return

    if finalOKr.get('status') == 'OK':
        print("registered device for user %s with otp %s"%(username, otp))
    else:
        print("NOT registered device for user %s with otp %s"%(username, otp))


def startDevice(username):
    req = requests.request('POST', globalIP,
                           data={'messageType': MessageType.DEVICE_ONLINE_INIT, 'username': username, 'deviceId': deviceID})

    if req.status_code != 200:
        print('can\'t get personal IP, request status $s'%req.status_code)
        return
    resp = req.json()
    if resp.get('messageType') != MessageType.DEVICE_ONLINE_GLOBAL_RETURN:
        print('bad message type %d, continuing...'%resp.get('messageType'))

    if 'pIP' not in resp:
        print('personal server IP not included, breaking...')
        exit(1)
    global personalIP
    personalIP = resp.get('pIP')

    finalOK = requests.request('POST', personalIP,
                               data = {'messageType':MessageType.DEVICE_ONLINE_CONNECT, 'username':username,
                                       'deviceId': deviceID})

    if finalOK.status_code != 200:
        print('can\'t connect Device, request status $s'%req.status_code)
        return
    finalOKr = finalOK.json()
    # if finalOKr.get('messageType') != MessageType.DEVICE_INIT_OK:
    #     print('bad message type %d, continuing...'%finalOKr.get('messageType'))
    #
    # if 'status' not in finalOKr:
    #     print('status not in final ok response')
    #     return
    #
    # if finalOKr.get('status') == 'OK':
    #     print("registered device for user %s with otp %s"%(username, otp))
    # else:
    #     print("NOT registered device for user %s with otp %s"%(username, otp))
    print("device connected for %s"%(username))
