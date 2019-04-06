import json
import socket

from flask import Flask, session, redirect, url_for, escape, request

from Common.MessageProperty import MessageProperty
from Common.MessageType import *
from Common import Sync
from Common.Security import decrypt, getPrivateKeyString
from PersonalServer import Controller, ToGlobal

app = Flask(__name__)
app.secret_key = 'any random string'

router = {
    MessageType.DEVICE_INIT_OK_TO_PERSONAL.value: Controller.deviceInitFromGlobal ,
    MessageType.DEVICE_INIT_CONNECT_TO_PERSONAL.value: Controller.deviceInitFromDevice,
    MessageType.DEVICE_ONLINE_CONNECT.value: Controller.connectDevice,
    MessageType.SYNC_REQUEST.value: Controller.syncRequest,
    MessageType.SYNC_CHECK.value: Controller.syncCheck,
}

myIPsocket = ''
username = ''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method != 'POST':
        print('not POST request')
        return 'not POST request'
    print('got message' + json.dumps(request.form))
    if MessageProperty.ENCRYPTED_MESSAGE.value not in request.form:
        print('no encrypted message included')
        return 'no encrypted message included'
    try:
        privateKey = getPrivateKeyString('D:\\dev\\pycharm\\SecureDropbox\\PersonalServer\\private_key.pem')
        requestForm = json.loads(decrypt(request.form[MessageProperty.ENCRYPTED_MESSAGE.value], privateKey))
    except:
        print('cant decrypt: '+request.form[MessageProperty.ENCRYPTED_MESSAGE.value])
        return 'cant decrypt'

    if MessageProperty.MESSAGE_TYPE.value not in requestForm:
        print('no message-type included')
        return 'no message-type included'
    if requestForm[MessageProperty.MESSAGE_TYPE.value] not in router:
        print("message-type %s not handled" % (requestForm[MessageProperty.MESSAGE_TYPE.value]))
        return "message-type %s not handled" % (requestForm[MessageProperty.MESSAGE_TYPE.value])
    return router.get(requestForm[MessageProperty.MESSAGE_TYPE.value])(requestForm)


def init(usernameTmp):
    global myIPsocket
    myIPsocket = socket.gethostbyname(socket.gethostname())+':5001'
    print("socket '%s'"%myIPsocket)
    global username
    username = usernameTmp
    ToGlobal.registerIPadress(username, myIPsocket)

    Sync.init('D:\dev\pycharm\personalSyncFolder')
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5001)
