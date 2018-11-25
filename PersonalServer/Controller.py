from flask import jsonify

from Common.MessageProperty import MessageProperty
from Common.MessageType import MessageType
from Common.Sync import *

def deviceInitFromGlobal(request):
    return "OK"



def deviceInitFromDevice(request):
    if MessageProperty.DEVICE_ID not in request:
        print(' bad new user request, no device-id provided')
        return jsonify({MessageProperty.MESSAGE_TYPE.value: MessageType.DEVICE_INIT_OK.value, MessageProperty.STATUS.value: 'no username'})

    if MessageProperty.DEVICE_PUBLIC_KEY.value not in request:
        print(' bad new user request, no device-public-key for personal server provided')
        return jsonify({MessageProperty.MESSAGE_TYPE.value: MessageType.DEVICE_INIT_OK.value,
                        MessageProperty.STATUS.value: 'no device-public-key'})

    if MessageProperty.ONE_TIME_PAD.value not in request:
        print(' bad new user request, no one time pad provided')
        return jsonify({MessageProperty.MESSAGE_TYPE.value: MessageType.DEVICE_INIT_OK.value, MessageProperty.STATUS.value: 'no otp'})

    if MessageProperty.USERNAME not in request:
        print(' bad new user request, no username provided')
        return jsonify({MessageProperty.MESSAGE_TYPE.value: MessageType.DEVICE_INIT_OK.value, MessageProperty.STATUS.value: 'no username'})

    addDeviceToLocalStorage(request.get(MessageProperty.DEVICE_ID.value),
                            request.get(MessageProperty.DEVICE_PUBLIC_KEY.value),
                            request.get(MessageProperty.ONE_TIME_PAD.value),
                            request.get(MessageProperty.USERNAME.value))

    return jsonify({MessageProperty.MESSAGE_TYPE.value: MessageType.DEVICE_INIT_OK.value, MessageProperty.STATUS.value: 'OK'})


def connectDevice(request):
    return jsonify({MessageProperty.MESSAGE_TYPE.value: MessageType.DEVICE_ONLINE_OK.value, MessageProperty.STATUS.value: 'OK'})


def addDeviceToLocalStorage(deviceId, devicePublicKey, OTP, username):
    with open('devices.txt', 'w') as file:
        file.write('deviceId:' + deviceId + ',' + 'devicePublicKey:' +
                devicePublicKey + ',' + 'OTP:' + OTP + ',' + 'username:' + username)


def readDevicesFromLocalStorage(deviceId, devicePublicKey):
    with open('devices.txt', 'r') as file:
        content = file.readlines()

    content = [x.strip() for x in content]

    for row in content:
        parts = row.split(',')

        storedDeviceId = parts[0].split(':')[1]
        storedDevicePublicKey = parts[1].split(':')[1]

        if deviceId == storedDeviceId:
            if devicePublicKey == storedDevicePublicKey:
                return jsonify({MessageProperty.MESSAGE_TYPE.value: MessageType.PERSONAL_INIT_OK.value, MessageProperty.STATUS.value: 'OK'})
            else:
                print('invalid device public key')
                return jsonify({MessageProperty.MESSAGE_TYPE.value: MessageType.PERSONAL_INIT_OK.value, MessageProperty.STATUS.value: 'invalid device public key'})

    print('device not found')
    return jsonify({MessageProperty.MESSAGE_TYPE.value: MessageType.PERSONAL_INIT_OK.value, MessageProperty.STATUS.value: 'no device found'})


def syncRequest(request):

    if MessageProperty.FILE_CHANGES_OBJECT.value not in request:
       print(' bad sync request, no file changes object')
       return jsonify({MessageProperty.MESSAGE_TYPE.value: MessageType.SYNC_CHECK_OK.value,
                       MessageProperty.STATUS.value: 'no file changes object'})

    for change in request.get(MessageProperty.FILE_CHANGES_OBJECT.value):
        applyChanges(change['path'], change.get['contents'])

    return jsonify({MessageProperty.MESSAGE_TYPE.value: MessageType.SYNC_CHECK_OK.value,
                    MessageProperty.STATUS.value: 'OK'})


def syncCheck(request):
    changes = checkChanges()
    print('personal server has changes=')
    print(changes)
    return jsonify({MessageProperty.MESSAGE_TYPE.value: MessageType.SYNC_CHECK_OK.value,
                    MessageProperty.FILE_CHANGES_OBJECT.value: changes,
                    MessageProperty.STATUS.value: 'OK'})
