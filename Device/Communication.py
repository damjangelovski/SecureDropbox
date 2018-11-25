import requests

from Common.MessageProperty import MessageProperty
from Common.MessageType import MessageType
from Common.Sync import *
from threading import Timer

globalIP = 'http://127.0.0.1:5000'
personalIP = ''
deviceID = 0
rootPath = 'D:\dev\pycharm\syncFolder'
refreshIntervalInSeconds = 3


def registerDevice(username, otp):
    req = requests.request('POST', globalIP, data={MessageProperty.MESSAGE_TYPE.value: MessageType.DEVICE_INIT_START.value,
                                                MessageProperty.USERNAME.value: username, MessageProperty.ONE_TIME_PAD.value: otp,
                                                   MessageProperty.DEVICE_PUBLIC_KEY.value: '123'})

    if req.status_code != 200:
        print('can\'t register Device, request status %s'%req.status_code)
        return
    resp = req.json()
    if resp.get(MessageProperty.MESSAGE_TYPE.value) != MessageType.DEVICE_INIT_OK_TO_DEVICE.value:
        print('bad message type %s, continuing...'%resp.get(MessageProperty.MESSAGE_TYPE.value))

    if MessageProperty.DEVICE_ID.value not in resp:
        print('id not included, continuing...')
    else:
        global deviceID
        deviceID = resp.get(MessageProperty.DEVICE_ID.value)
        print("this device id is %d"%deviceID)

    if MessageProperty.PERSONAL_IP_SOCKET.value not in resp:
        print('personal server IP not included, breaking...')
        return
    global personalIP
    personalIP = resp.get(MessageProperty.PERSONAL_IP_SOCKET.value)

    finalOK = requests.request('POST', 'http://'+personalIP,
                               data = {MessageProperty.MESSAGE_TYPE.value:MessageType.DEVICE_INIT_CONNECT_TO_PERSONAL.value,
                            MessageProperty.USERNAME.value:username,MessageProperty.ONE_TIME_PAD.value:otp,
                           MessageProperty.DEVICE_ID.value: deviceID, MessageProperty.DEVICE_PUBLIC_KEY.value: '123'})

    if finalOK.status_code != 200:
        print('can\'t register Device, request status %s'%finalOK.status_code)
        return
    finalOKr = finalOK.json()
    if finalOKr.get(MessageProperty.MESSAGE_TYPE.value) != MessageType.DEVICE_INIT_OK.value:
        print('bad message type %s, continuing...'%finalOKr.get(MessageProperty.MESSAGE_TYPE.value))

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
        print('can\'t get personal IP, request status %s'%req.status_code)
        return
    resp = req.json()
    if resp.get(MessageProperty.MESSAGE_TYPE.value) != MessageType.DEVICE_ONLINE_GLOBAL_RETURN:
        print('bad message type %s, continuing...'%resp.get(MessageProperty.MESSAGE_TYPE.value))

    if MessageProperty.PERSONAL_IP_SOCKET.value not in resp:
        print('personal server IP not included, breaking...')
        exit(1)
    global personalIP
    personalIP = resp.get(MessageProperty.PERSONAL_IP_SOCKET.value)

    finalOK = requests.request('POST', 'http://'+personalIP, data={MessageProperty.MESSAGE_TYPE.value:MessageType.DEVICE_ONLINE_CONNECT,
                                                MessageProperty.USERNAME.value:username, MessageProperty.DEVICE_ID.value: deviceID})

    if finalOK.status_code != 200:
        print('can\'t connect Device, request status %s'%req.status_code)
        return
    finalOKr = finalOK.json()
    if finalOKr.get(MessageProperty.MESSAGE_TYPE.value) != MessageType.DEVICE_ONLINE_OK:
        print('bad message type %s, continuing...'%finalOKr.get(MessageProperty.MESSAGE_TYPE.value))

    if MessageProperty.STATUS.value not in finalOKr:
        print('status not in final ok response')
        return

    if finalOKr.get(MessageProperty.STATUS.value) != 'OK':
        print("personal server refused connection for  user %s"%(username))
        exit(1)

    print("device connected for %s"%(username))

    init(rootPath)
    Timer(refreshIntervalInSeconds, syncWithPersonal(username)).start()

def syncWithPersonal(username):

    changes = checkChanges()
    print('device has changes='+changes)

    if len(changes) > 0:

        syncReq = requests.request('POST', 'http://'+personalIP, data={MessageProperty.MESSAGE_TYPE.value:MessageType.SYNC_REQUEST,
                                                MessageProperty.USERNAME.value:username, MessageProperty.DEVICE_ID.value: deviceID,
                                                MessageProperty.FILE_CHANGES_OBJECT: changes})
        if syncReq.status_code != 200:
            print('can\'t connect Device, request status %s' % syncReq.status_code)
            return
        syncReqr = syncReq.json()
        if syncReqr.get(MessageProperty.MESSAGE_TYPE.value) != MessageType.SYNC_REQUEST_OK:
            print('bad message type %s, continuing...' % syncReqr.get(MessageProperty.MESSAGE_TYPE.value))

        if MessageProperty.STATUS.value not in syncReqr:
            print('status not in final ok response')
            return

        if syncReqr.get(MessageProperty.STATUS.value) != 'OK':
            print("personal server refused sync for  user %s" % (username))
            return

        print("device connected for %s" % (username))

    syncCheckReq = requests.request('POST', 'http://'+personalIP, data={MessageProperty.MESSAGE_TYPE.value:MessageType.SYNC_CHECK,
                                                MessageProperty.USERNAME.value:username, MessageProperty.DEVICE_ID.value: deviceID})

    if syncCheckReq.status_code != 200:
        print('can\'t connect Device, request status %s'%syncCheckReq.status_code)
        return
    syncCheckReqr = syncCheckReq.json()
    if syncCheckReqr.get(MessageProperty.MESSAGE_TYPE.value) != MessageType.SYNC_CHECK_OK:
        print('bad message type %s, continuing...'%syncCheckReqr.get(MessageProperty.MESSAGE_TYPE.value))

    if MessageProperty.STATUS.value not in syncCheckReqr:
        print('status not in final ok response')
        return

    if syncCheckReqr.get(MessageProperty.STATUS.value) != 'OK':
        print("personal server refused connection for  user %s"%(username))
        return

    for change in syncCheckReqr.get(MessageProperty.FILE_CHANGES_OBJECT):
        applyChanges(change['path'], change.get['contents'])