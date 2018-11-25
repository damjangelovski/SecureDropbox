from flask import jsonify
from Common.MessageType import MessageType
from Common.MessageProperty import MessageProperty
from GlobalServer import SQLiteRepo as repo


def addNewUser(request):

    if MessageProperty.USERNAME.value not in request:
        print(' bad new user request, no username provided')
        return jsonify({MessageProperty.MESSAGE_TYPE.value: MessageType.PERSONAL_INIT_OK.value,
                        MessageProperty.STATUS.value: 'no username'})

    if MessageProperty.PERSONAL_PUBLIC_KEY.value not in request:
        print(' bad new user request, no public key for personal server provided')
        return jsonify({'messageType': MessageType.PERSONAL_INIT_OK.value, 'status': 'no personal-public-key'})

    repo.setNewUser(request.get(MessageProperty.USERNAME.value), request.get(MessageProperty.PERSONAL_PUBLIC_KEY.value))

    return jsonify({MessageProperty.MESSAGE_TYPE.value: MessageType.PERSONAL_INIT_OK.value, MessageProperty.STATUS.value: 'OK'})


def addPersonalServerIPadress(request):
    if MessageProperty.USERNAME.value not in request:
        print(' bad new user request, no username provided')
        return jsonify({MessageProperty.MESSAGE_TYPE.value: MessageType.PERSONAL_INIT_OK.value,
                        MessageProperty.STATUS.value: 'no username'})

    if MessageProperty.PERSONAL_IP_SOCKET.value not in request:
        print(' bad new user request, no IP socket personal server provided')
        return jsonify({MessageProperty.MESSAGE_TYPE.value: MessageType.PERSONAL_INIT_OK.value,
                        MessageProperty.STATUS.value: 'no personal-IP'})

    repo.setIP(request.get(MessageProperty.USERNAME.value), request.get(MessageProperty.PERSONAL_IP_SOCKET.value))

    return jsonify({MessageProperty.MESSAGE_TYPE.value: MessageType.PERSONAL_INIT_OK.value, MessageProperty.STATUS.value: 'OK'})


def addOTPforNewDevice(request):
    if MessageProperty.USERNAME.value not in request:
        print(' bad new user request, no username provided')
        return jsonify({MessageProperty.MESSAGE_TYPE.value: MessageType.PERSONAL_INIT_OK.value,
                        MessageProperty.STATUS.value: 'no username'})

    if MessageProperty.ONE_TIME_PAD.value not in request:
        print(' bad new user request, no one time pad provided')
        return jsonify({MessageProperty.MESSAGE_TYPE.value: MessageType.PERSONAL_INIT_OK.value, MessageProperty.STATUS.value: 'no otp'})

    repo.setIP(request.get(MessageProperty.USERNAME.value), request.get(MessageProperty.ONE_TIME_PAD.value))

    return jsonify({MessageProperty.MESSAGE_TYPE.value: MessageType.PERSONAL_INIT_OK.value, MessageProperty.STATUS.value: 'OK'})


def getAllUsers():
    return repo.getUsers()