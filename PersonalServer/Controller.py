from flask import jsonify
from Common.MessageType import MessageType

def deviceInitFromGlobal(request):
    return "OK"



def deviceInitFromDevice(request):
    if 'device-id' not in request:
        print(' bad new user request, no device-id provided')
        return jsonify(messageType=MessageType.PERSONAL_INIT_OK.value, status='no username')

    if 'device-public-key' not in request:
        print(' bad new user request, no device-public-key for personal server provided')
        return jsonify(messageType=MessageType.PERSONAL_INIT_OK, status='no personal-public-key')

    if 'otp' not in request:
        print(' bad new user request, no one time pad provided')
        return jsonify(messageType=MessageType.PERSONAL_INIT_OK, status='no otp')

    if 'username' not in request:
        print(' bad new user request, no username provided')
        return jsonify(messageType=MessageType.PERSONAL_INIT_OK.value, status='no username')

    addDeviceToLocalStorage(request.get('device-id'), request.get('device-public-key'), request.get('username'))


def connectDevice(request):
    return 'OK'


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
                return jsonify(messageType=MessageType.PERSONAL_INIT_OK.value, status='OK')
            else:
                print('invalid device public key')
                return jsonify(messageType=MessageType.PERSONAL_INIT_OK.value, status='invalid device public key')

    print('device not found')
    return jsonify(messageType=MessageType.PERSONAL_INIT_OK.value, status='no device found')