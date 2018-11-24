import requests
from flask import jsonify

from Common.MessageType import MessageType
from GlobalServer import SQLiteRepo as repo

def addDevice(request):

    if 'username' not in request:
        print(' bad new user request, no username provided')
        return jsonify(messageType=MessageType.PERSONAL_INIT_OK.value, status='no username')
    username = request.get('username')

    if 'otp' not in request:
        print(' bad new user request, no one time pad provided')
        return jsonify(messageType=MessageType.PERSONAL_INIT_OK, status='no otp')

    if 'device-public-key' not in request:
        print(' bad new user request, no public key for device provided')
        return jsonify(messageType=MessageType.PERSONAL_INIT_OK, status='no device-public-key')

    repo.setDevice(1, username, request.get('device-public-key'))

    personalIP = repo.getIP(username)
    if personalIP != '':
        requests.request(requests.request('POST', personalIP,
                           data={'messageType': MessageType.DEVICE_INIT_OK_TO_PERSONAL, 'username': username,
                                 'deviceId': 1}))

    return jsonify(messageType=MessageType.DEVICE_INIT_OK_TO_DEVICE.value, status='OK')

def getPersonalServerIPadress(request):

    if 'username' not in request:
        print(' bad new user request, no username provided')
        return jsonify(messageType=MessageType.PERSONAL_INIT_OK.value, status='no username')

    if 'deviceId' not in request:
        print(' bad new user request, no ID for device provided')
        return jsonify(messageType=MessageType.PERSONAL_INIT_OK, status='no deviceId')

    IP = repo.getIP(request.get('username'))

    return jsonify(messageType=MessageType.DEVICE_ONLINE_GLOBAL_RETURN.value, status='OK', personalIp=IP)
