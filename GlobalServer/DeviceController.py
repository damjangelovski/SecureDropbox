import requests
from flask import jsonify

from Common.MessageProperty import MessageProperty
from Common.MessageType import MessageType
from GlobalServer import SQLiteRepo as repo

def addDevice(request):

    if MessageProperty.USERNAME not in request:
        print(' bad new user request, no username provided')
        return jsonify(messageType=MessageType.PERSONAL_INIT_OK.value, status='no username')
    username = request.get(MessageProperty.USERNAME)

    if MessageProperty.ONE_TIME_PAD not in request:
        print(' bad new user request, no one time pad provided')
        return jsonify(messageType=MessageType.PERSONAL_INIT_OK, M='no otp')

    if MessageProperty.DEVICE_PUBLIC_KEY not in request:
        print(' bad new user request, no public key for device provided')
        return jsonify(messageType=MessageType.PERSONAL_INIT_OK, status='no device-public-key')

    repo.setDevice(1, username, request.get(MessageProperty.DEVICE_PUBLIC_KEY))

    personalIP = repo.getIP(username)
    if personalIP != '':
        requests.request(requests.request('POST', personalIP,
                           data={MessageProperty.MESSAGE_TYPE: MessageType.DEVICE_INIT_OK_TO_PERSONAL.value, MessageProperty.USERNAME: username,
                                 MessageProperty.DEVICE_ID: 1}))

    return jsonify(messageType=MessageType.DEVICE_INIT_OK_TO_DEVICE.value, status='OK')

def getPersonalServerIPadress(request):

    if MessageProperty.USERNAME not in request:
        print(' bad new user request, no username provided')
        return jsonify(messageType=MessageType.PERSONAL_INIT_OK.value, status='no username')

    if MessageProperty.DEVICE_ID not in request:
        print(' bad new user request, no ID for device provided')
        return jsonify(messageType=MessageType.PERSONAL_INIT_OK, status='no deviceId')

    IP = repo.getIP(request.get(MessageProperty.USERNAME))

    return jsonify(messageType=MessageType.DEVICE_ONLINE_GLOBAL_RETURN.value, status='OK', personalIp=IP)


def getAllDevices():
    return repo.getDevices()