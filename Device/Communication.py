from Common.Communication import *
from Common.MessageProperty import MessageProperty
from Common.MessageType import MessageType
from Common.Sync import *

personalIP = ''
personalPK = ''
deviceID = 0
rootPath = 'D:\dev\pycharm\deviceSyncFolder'
refreshIntervalInSeconds = 3


def registerDevice(username, otp):
    req = sendEncryptedMessageToGlobal({MessageProperty.MESSAGE_TYPE.value: MessageType.DEVICE_INIT_START.value,
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
    if MessageProperty.PERSONAL_PUBLIC_KEY.value not in resp:
        print('personal server public key not included, breaking...')
        return
    global personalPK
    personalIP = resp.get(MessageProperty.PERSONAL_IP_SOCKET.value)
    personalPK = resp.get(MessageProperty.PERSONAL_PUBLIC_KEY.value)

    finalOK = sendEncryptedMessage(
        'http://' + personalIP,
        {MessageProperty.MESSAGE_TYPE.value: MessageType.DEVICE_INIT_CONNECT_TO_PERSONAL.value,
            MessageProperty.USERNAME.value: username, MessageProperty.ONE_TIME_PAD.value: otp,
            MessageProperty.DEVICE_ID.value: deviceID, MessageProperty.DEVICE_PUBLIC_KEY.value: '123'},
        personalPK)

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
    req = sendEncryptedMessageToGlobal({
        MessageProperty.MESSAGE_TYPE.value: MessageType.DEVICE_ONLINE_INIT.value,
        MessageProperty.USERNAME.value: username,
        MessageProperty.DEVICE_ID.value: deviceID})

    if req.status_code != 200:
        print('can\'t get personal IP, request status %s'%req.status_code)
        return
    resp = req.json()
    if resp.get(MessageProperty.MESSAGE_TYPE.value) != MessageType.DEVICE_ONLINE_GLOBAL_RETURN.value:
        print('bad message type %s, continuing...'%resp.get(MessageProperty.MESSAGE_TYPE.value))

    if MessageProperty.PERSONAL_IP_SOCKET.value not in resp:
        print('personal server IP not included, breaking...')
        exit(1)
    global personalIP
    personalIP = resp.get(MessageProperty.PERSONAL_IP_SOCKET.value)

    if MessageProperty.PERSONAL_PUBLIC_KEY.value not in resp:
        print('personal server PK not included, breaking...')
        exit(1)
    global personalPK
    personalPK = resp.get(MessageProperty.PERSONAL_PUBLIC_KEY.value)

    finalOK = sendEncryptedMessage('http://'+personalIP,
        {MessageProperty.MESSAGE_TYPE.value:MessageType.DEVICE_ONLINE_CONNECT.value,
            MessageProperty.USERNAME.value:username,
            MessageProperty.DEVICE_ID.value: deviceID},
        personalPK)

    if finalOK.status_code != 200:
        print('can\'t connect Device, request status %s'%req.status_code)
        return
    finalOKr = finalOK.json()
    if finalOKr.get(MessageProperty.MESSAGE_TYPE.value) != MessageType.DEVICE_ONLINE_OK.value:
        print('bad message type %s, continuing...'%finalOKr.get(MessageProperty.MESSAGE_TYPE.value))

    if MessageProperty.STATUS.value not in finalOKr:
        print('status not in final ok response')
        return

    if finalOKr.get(MessageProperty.STATUS.value) != 'OK':
        print("personal server refused connection for  user %s"%(username))
        exit(1)

    print("device connected for %s"%(username))

    init(rootPath)

    # Timer(refreshIntervalInSeconds, syncWithPersonal(username)).start()
    while True:
        syncWithPersonal(username)
        time.sleep(refreshIntervalInSeconds)

def syncWithPersonal(username):

    changes = checkChanges()
    if(changes != []):
        print('device has changes=' + str(changes))

    if len(changes) > 0:

        syncReq = sendEncryptedMessage('http://'+personalIP,
        {MessageProperty.MESSAGE_TYPE.value: MessageType.SYNC_REQUEST.value,
            MessageProperty.USERNAME.value: username,
            MessageProperty.DEVICE_ID.value: deviceID,
            MessageProperty.FILE_CHANGES_OBJECT.value: changes},
        personalPK)

        if syncReq.status_code != 200:
            print('can\'t connect Device, request status %s' % syncReq.status_code)
            return
        syncReqr = syncReq.json()
        if syncReqr.get(MessageProperty.MESSAGE_TYPE.value) != MessageType.SYNC_REQUEST_OK.value:
            print('bad message type %s, continuing...' % syncReqr.get(MessageProperty.MESSAGE_TYPE.value))

        if MessageProperty.STATUS.value not in syncReqr:
            print('status not in final ok response')
            return

        if syncReqr.get(MessageProperty.STATUS.value) != 'OK':
            print("personal server refused sync for  user %s" % (username))
            return

        print("device connected for %s" % (username))

    syncCheckReq = sendEncryptedMessage('http://'+personalIP,
        {MessageProperty.MESSAGE_TYPE.value: MessageType.SYNC_CHECK.value,
            MessageProperty.USERNAME.value: username,
            MessageProperty.DEVICE_ID.value: deviceID},
        personalPK)

    if syncCheckReq.status_code != 200:
        print('can\'t connect Device, request status %s'%syncCheckReq.status_code)
        return
    syncCheckReqr = syncCheckReq.json()
    if syncCheckReqr.get(MessageProperty.MESSAGE_TYPE.value) != MessageType.SYNC_CHECK_OK.value:
        print('bad message type %s, continuing...'%syncCheckReqr.get(MessageProperty.MESSAGE_TYPE.value))

    if MessageProperty.STATUS.value not in syncCheckReqr:
        print('status not in final ok response')
        return

    if syncCheckReqr.get(MessageProperty.STATUS.value) != 'OK':
        print("personal server refused connection for  user %s"%(username))
        return

    for change in syncCheckReqr.get(MessageProperty.FILE_CHANGES_OBJECT.value):
        applyChanges(change['path'], change['contents'])