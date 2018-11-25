import requests
from flask import jsonify

from Common.MessageProperty import MessageProperty
from Common.MessageType import MessageType
from GlobalServer import SQLiteRepo as repo

def addDevice(request):

    if MessageProperty.USERNAME.value not in request:
        print(' bad new device request, no username provided')
        return jsonify({MessageProperty.MESSAGE_TYPE.value: MessageType.DEVICE_INIT_OK_TO_DEVICE.value,
                        MessageProperty.STATUS.value: 'no username'})
    username = request.get(MessageProperty.USERNAME.value)

    if MessageProperty.ONE_TIME_PAD.value not in request:
        print(' bad new device request, no one time pad provided')
        return jsonify({MessageProperty.MESSAGE_TYPE.value: MessageType.DEVICE_INIT_OK_TO_DEVICE.value, MessageProperty.STATUS.value: 'no otp'})

    if MessageProperty.DEVICE_PUBLIC_KEY.value not in request:
        print(' bad new device request, no public key for device provided')
        return jsonify({MessageProperty.MESSAGE_TYPE.value: MessageType.DEVICE_INIT_OK_TO_DEVICE.value,
                        MessageProperty.STATUS.value: 'no device-public-key'})

    deviceId = repo.setDevice(username, request.get(MessageProperty.DEVICE_PUBLIC_KEY.value))

    personalIP = repo.getIP(username)
    if personalIP != '':
        url = 'http://' + personalIP
        requests.request('POST', url, data={MessageProperty.MESSAGE_TYPE.value: MessageType.DEVICE_INIT_OK_TO_PERSONAL.value,
                                 MessageProperty.USERNAME.value: username, MessageProperty.DEVICE_ID.value: deviceId})

    return jsonify({MessageProperty.MESSAGE_TYPE.value: MessageType.DEVICE_INIT_OK_TO_DEVICE.value, MessageProperty.DEVICE_ID.value: deviceId,
                    MessageProperty.PERSONAL_IP_SOCKET.value: personalIP, MessageProperty.STATUS.value: 'OK'})

def getPersonalServerIPadress(request):

    if MessageProperty.USERNAME.value not in request:
        print(' bad get IP request, no username provided')
        return jsonify({MessageProperty.MESSAGE_TYPE.value: MessageType.DEVICE_ONLINE_GLOBAL_RETURN.value,
                        MessageProperty.STATUS.value: 'no username'})

    if MessageProperty.DEVICE_ID.value not in request:
        print(' bad get IP request, no ID for device provided')
        return jsonify({MessageProperty.MESSAGE_TYPE.value: MessageType.DEVICE_ONLINE_GLOBAL_RETURN.value,
                        MessageProperty.STATUS.value: 'no deviceId'})

    IP = repo.getIP(request.get(MessageProperty.USERNAME.value))

    return jsonify({MessageProperty.MESSAGE_TYPE.value: MessageType.DEVICE_ONLINE_GLOBAL_RETURN.value,
                    MessageProperty.STATUS.value: 'OK', MessageProperty.PERSONAL_IP_SOCKET.value: IP})


def getAllDevices():
    return repo.getDevices()
