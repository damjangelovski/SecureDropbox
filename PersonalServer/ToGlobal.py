import requests
import random

from Common.MessageProperty import MessageProperty
from Common.MessageType import MessageType

# globalIP = '192.168.1.50:5000'
globalIP = 'http://127.0.0.1:5000/'

def addNewUser(username):
    req = requests.request('POST', globalIP,
                           data={MessageProperty.MESSAGE_TYPE.value: MessageType.PERSONAL_INIT_INIT.value, MessageProperty.USERNAME.value: username,
                                 MessageProperty.PERSONAL_PUBLIC_KEY.value: '123'})

    if req.status_code != 200:
        print('can\'t register user, request status %s' % req.status_code)
        exit(1)
    resp = req.json()
    if resp.get(MessageProperty.MESSAGE_TYPE.value) != MessageType.PERSONAL_INIT_OK.value:
        print('bad message type %s, continuing...' % resp.get(MessageProperty.MESSAGE_TYPE.value))

    if MessageProperty.STATUS.value not in resp:
        print('status not in response')
        return

    if resp.get(MessageProperty.STATUS.value) == 'OK':
        print("added new user "+username)
    else:
        print("NOT added new user "+username)


def registerIPadress(username, address):
    req = requests.request('POST', globalIP, data={MessageProperty.MESSAGE_TYPE.value: MessageType.PERSONAL_ONLINE_INIT.value,
                                       MessageProperty.USERNAME.value: username, MessageProperty.PERSONAL_IP_SOCKET.value: address})

    if req.status_code != 200:
        print('can\'t register IP, request status %s' % req.status_code)
        exit(1)
    resp = req.json()
    if resp.get(MessageProperty.MESSAGE_TYPE.value) != MessageType.PERSONAL_ONLINE_OK:
        print('bad message type %s, continuing...' % resp.get(MessageProperty.MESSAGE_TYPE.value))

    if MessageProperty.STATUS.value not in resp:
        print('status not in response')
        return

    if resp.get(MessageProperty.STATUS.value) == 'OK':
        print('ID address %s for user %s registered' % (address, username))
    else:
        print('ID address %s for user %s NOT registered' % (address, username))


def addDevice(username, otp):
    req = requests.request('POST', globalIP,
                           data={MessageProperty.MESSAGE_TYPE.value: MessageType.DEVICE_INIT_INIT.value, MessageProperty.USERNAME.value: username, MessageProperty.ONE_TIME_PAD.value: otp})

    if req.status_code != 200:
        print('can\'t register user, request status $s' % req.status_code)
        exit(1)
    resp = req.json()
    if resp.get(MessageProperty.MESSAGE_TYPE.value) != MessageType.PERSONAL_INIT_OK:
        print('bad message type %d, continuing...' % resp.get(MessageProperty.MESSAGE_TYPE.value))

    if MessageProperty.STATUS.value not in resp:
        print('status not in response')
        return

    if resp.get(MessageProperty.STATUS.value) == 'OK':
        print("added new user " + username)
    else:
        print("NOT added new user " + username)
    print("sent new device OTP to global for user %s" % username)
