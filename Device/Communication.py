import requests

from Common.MessageProperty import MessageProperty
from Common.MessageType import MessageType

globalIP = '127.0.0.1:5000'
personalIP = ''
deviceID = 0

def registerDevice(username, otp):
    req = requests.request('POST', globalIP, data={MessageProperty.MESSAGE_TYPE.value: MessageType.DEVICE_INIT_START.value,
                                                MessageProperty.USERNAME.value: username, MessageProperty.ONE_TIME_PAD.value: otp})

    if req.status_code != 200:
        print('can\'t register Device, request status $s'%req.status_code)
        return
    resp = req.json()
    if resp.get(MessageProperty.MESSAGE_TYPE.value) != MessageType.DEVICE_INIT_OK_TO_DEVICE:
        print('bad message type %d, continuing...'%resp.get(MessageProperty.MESSAGE_TYPE.value))

    if MessageProperty.DEVICE_ID.value not in resp:
        print('id not included, continuing...')
    else:
        global deviceID
        deviceID = resp.get(MessageProperty.DEVICE_ID.value)
        print("id is %d"%deviceID)

    if MessageProperty.PERSONAL_IP_SOCKET.value not in resp:
        print('personal server IP not included, breaking...')
        return
    global personalIP
    personalIP = resp.get(MessageProperty.PERSONAL_IP_SOCKET.value)

    finalOK = requests.request('POST', personalIP,
                               data = {MessageProperty.MESSAGE_TYPE.value:MessageType.DEVICE_INIT_CONNECT_TO_PERSONAL.value,
                            MessageProperty.USERNAME.value:username,MessageProperty.ONE_TIME_PAD.value:otp, MessageProperty.DEVICE_ID.value:deviceID})

    if finalOK.status_code != 200:
        print('can\'t register Device, request status $s'%req.status_code)
        return
    finalOKr = finalOK.json()
    if finalOKr.get(MessageProperty.MESSAGE_TYPE.value) != MessageType.DEVICE_INIT_OK:
        print('bad message type %d, continuing...'%finalOKr.get(MessageProperty.MESSAGE_TYPE.value))

    if MessageProperty.STATUS.value not in finalOKr:
        print('status not in final ok response')
        return

    if finalOKr.get(MessageProperty.STATUS.value) == 'OK':
        print("registered device for user %s with otp %s"%(username, otp))
    else:
        print("NOT registered device for user %s with otp %s"%(username, otp))


def startDevice(username):
    req = requests.request('POST', globalIP, data={MessageProperty.MESSAGE_TYPE.value: MessageType.DEVICE_ONLINE_INIT.value,
                                            MessageProperty.USERNAME.value: username, MessageProperty.DEVICE_ID.value: deviceID})

    if req.status_code != 200:
        print('can\'t get personal IP, request status $s'%req.status_code)
        return
    resp = req.json()
    if resp.get(MessageProperty.MESSAGE_TYPE.value) != MessageType.DEVICE_ONLINE_GLOBAL_RETURN:
        print('bad message type %d, continuing...'%resp.get(MessageProperty.MESSAGE_TYPE.value))

    if MessageProperty.PERSONAL_IP_SOCKET.value not in resp:
        print('personal server IP not included, breaking...')
        exit(1)
    global personalIP
    personalIP = resp.get(MessageProperty.PERSONAL_IP_SOCKET.value)

    finalOK = requests.request('POST', personalIP, data={MessageProperty.MESSAGE_TYPE.value:MessageType.DEVICE_ONLINE_CONNECT,
                                                MessageProperty.USERNAME.value:username, MessageProperty.DEVICE_ID.value: deviceID})

    if finalOK.status_code != 200:
        print('can\'t connect Device, request status $s'%req.status_code)
        return
    finalOKr = finalOK.json()
    # if finalOKr.get(MessageProperty.MESSAGE_TYPE.value) != MessageType.DEVICE_INIT_OK:
    #     print('bad message type %d, continuing...'%finalOKr.get(MessageProperty.MESSAGE_TYPE.value))
    #
    # if MessageProperty.STATUS.value not in finalOKr:
    #     print('status not in final ok response')
    #     return
    #
    # if finalOKr.get(MessageProperty.STATUS.value) == 'OK':
    #     print("registered device for user %s with otp %s"%(username, otp))
    # else:
    #     print("NOT registered device for user %s with otp %s"%(username, otp))
    print("device connected for %s"%(username))
