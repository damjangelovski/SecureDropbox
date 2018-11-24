from flask import jsonify
from Common.MessageType import MessageType
from GlobalServer import SQLiteRepo as repo


def addNewUser(request):

    if MessageProperty.USERNAME not in request:
        print(' bad new user request, no username provided')
        return jsonify(messageType=MessageType.PERSONAL_INIT_OK.value, status='no username')

    if MessageProperty.PERSONAL_PUBLIC_KEY not in request:
        print(' bad new user request, no public key for personal server provided')
        return jsonify(messageType=MessageType.PERSONAL_INIT_OK.value, status='no personal-public-key')

    repo.setNewUser(request.get(MessageProperty.USERNAME), request.get(MessageProperty.PERSONAL_PUBLIC_KEY))

    return jsonify(messageType=MessageType.PERSONAL_INIT_OK.value, status='OK')


def addPersonalServerIPadress(request):
    if MessageProperty.USERNAME not in request:
        print(' bad new user request, no username provided')
        return jsonify(messageType=MessageType.PERSONAL_INIT_OK, status='no username')

    if 'personal_IP' not in request:
        print(' bad new user request, no IP socket personal server provided')
        return jsonify(messageType=MessageType.PERSONAL_INIT_OK, status='no personal-IP')

    repo.setIP(request.get(MessageProperty.USERNAME), request.get('personal_IP'))

    return jsonify(messageType=MessageType.PERSONAL_INIT_OK, status='OK')


def addOTPforNewDevice(request):
    if MessageProperty.USERNAME not in request:
        print(' bad new user request, no username provided')
        return jsonify(messageType=MessageType.PERSONAL_INIT_OK, status='no username')

    if MessageProperty.ONE_TIME_PAD not in request:
        print(' bad new user request, no one time pad provided')
        return jsonify(messageType=MessageType.PERSONAL_INIT_OK, status='no otp')

    repo.setIP(request.get(MessageProperty.USERNAME), request.get(MessageProperty.ONE_TIME_PAD))

    return jsonify(messageType=MessageType.PERSONAL_INIT_OK, status='OK')


def getAllUsers():
    return repo.getUsers()