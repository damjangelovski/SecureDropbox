import requests
import random
from Common.MessageType import MessageType

globalIP = '127.0.0.1:500'

def addNewUser(username):
    req = requests.request('POST', globalIP,
                           data={'messageType': MessageType.PERSONAL_INIT_INIT, 'username': username, 'public-key': '123'})

    if req.status_code != 200:
        print('can\'t register user, request status $s' % req.status_code)
        exit(1)
    resp = req.json()
    if resp.get('messageType') != MessageType.PERSONAL_INIT_OK:
        print('bad message type %d, continuing...' % resp.get('messageType'))

    if 'status' not in resp:
        print('status not in response')
        return

    if resp.get('status') == 'OK':
        print("added new user "+username)
    else:
        print("NOT added new user "+username)

def registerIPadress(username, address):
    req = requests.request('POST', globalIP,
                           data={'messageType': MessageType.PERSONAL_ONLINE_INIT, 'username': username,
                                 'personal-ip': address})

    if req.status_code != 200:
        print('can\'t register IP, request status $s' % req.status_code)
        exit(1)
    resp = req.json()
    if resp.get('messageType') != MessageType.PERSONAL_ONLINE_OK:
        print('bad message type %d, continuing...' % resp.get('messageType'))

    if 'status' not in resp:
        print('status not in response')
        return

    if resp.get('status') == 'OK':
        print('ID address %s for user %s registered' % (address, username))
    else:
        print('ID address %s for user %s NOT registered' % (address, username))

def addDevice(username, otp):
    req = requests.request('POST', globalIP,
                           data={'messageType': MessageType.DEVICE_INIT_INIT, 'username': username,
                                 'otp': otp})

    if req.status_code != 200:
        print('can\'t register user, request status $s' % req.status_code)
        exit(1)
    resp = req.json()
    if resp.get('messageType') != MessageType.PERSONAL_INIT_OK:
        print('bad message type %d, continuing...' % resp.get('messageType'))

    if 'status' not in resp:
        print('status not in response')
        return

    if resp.get('status') == 'OK':
        print("added new user " + username)
    else:
        print("NOT added new user " + username)
    print("sent new device OTP to global for user %s" % username)
