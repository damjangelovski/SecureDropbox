from flask import jsonify
from Common.MessageType import MessageType
from GlobalServer import SQLiteRepo as repo


def addNewUser(request):

    if 'username' not in request:
        print(' bad new user request, no username provided')
        return jsonify(messageType=MessageType.PERSONAL_INIT_OK.value, status='no username')

    if 'personal-public-key' not in request:
        print(' bad new user request, no public key for personal server provided')
        return jsonify(messageType=MessageType.PERSONAL_INIT_OK, status='no personal-public-key')

    repo.setNewUser(request.get('username'), request.get('personal-public-key'))

    return jsonify(messageType=MessageType.PERSONAL_INIT_OK.value, status='OK')


def addPersonalServerIPadress(request):
    if 'username' not in request:
        print(' bad new user request, no username provided')
        return jsonify(messageType=MessageType.PERSONAL_INIT_OK, status='no username')

    if 'personal_IP' not in request:
        print(' bad new user request, no IP socket personal server provided')
        return jsonify(messageType=MessageType.PERSONAL_INIT_OK, status='no personal-IP')

    repo.setIP(request.get('username'), request.get('personal_IP'))

    return jsonify(messageType=MessageType.PERSONAL_INIT_OK, status='OK')


def addOTPforNewDevice(request):
    if 'username' not in request:
        print(' bad new user request, no username provided')
        return jsonify(messageType=MessageType.PERSONAL_INIT_OK, status='no username')

    if 'otp' not in request:
        print(' bad new user request, no one time pad provided')
        return jsonify(messageType=MessageType.PERSONAL_INIT_OK, status='no otp')

    repo.setIP(request.get('username'), request.get('otp'))

    return jsonify(messageType=MessageType.PERSONAL_INIT_OK, status='OK')


def getAllUsers():
    return repo.getUsers()